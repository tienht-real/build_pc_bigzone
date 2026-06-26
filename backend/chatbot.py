"""
Chatbot AI tư vấn sản phẩm cho Bigzone.

Dùng Claude (model claude-opus-4-8) với tool use để truy vấn dữ liệu sản phẩm
thật trong CSDL, và stream câu trả lời về client qua SSE.
"""
import json
import logging
import os

from sqlalchemy import or_
from sqlalchemy.orm import Session

import models

logger = logging.getLogger("bigzone.chatbot")

MODEL = "claude-opus-4-8"
MAX_TOOL_ROUNDS = 5

# Lazy import + khởi tạo client để web vẫn chạy được khi chưa cài/đặt key.
_client = None
_client_ready = False


def get_client():
    """Trả về Anthropic client, hoặc None nếu thiếu key / chưa cài SDK."""
    global _client, _client_ready
    if _client_ready:
        return _client
    _client_ready = True
    if not os.environ.get("ANTHROPIC_API_KEY"):
        logger.warning("Thiếu ANTHROPIC_API_KEY — chatbot bị tắt.")
        _client = None
        return None
    try:
        import anthropic
        _client = anthropic.Anthropic()
    except Exception as e:  # SDK chưa cài hoặc lỗi khởi tạo
        logger.warning("Không khởi tạo được Anthropic client: %s", e)
        _client = None
    return _client


# ── Định nghĩa tool tìm sản phẩm ─────────────────────────────────────────────
SEARCH_PRODUCTS_TOOL = {
    "name": "search_products",
    "description": (
        "Tìm sản phẩm trong cửa hàng Bigzone theo danh mục, từ khoá và khoảng giá. "
        "Luôn dùng tool này để lấy dữ liệu sản phẩm THẬT trước khi tư vấn — "
        "không được tự bịa ra sản phẩm, giá hay thông số."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "category_id": {
                "type": "integer",
                "description": "ID danh mục cần lọc (xem danh sách danh mục trong hướng dẫn). Bỏ trống nếu không chắc.",
            },
            "keyword": {
                "type": "string",
                "description": "Từ khoá tìm theo tên/thương hiệu/mô tả, ví dụ 'RTX 4060', 'laptop', 'gaming'.",
            },
            "min_price": {
                "type": "integer",
                "description": "Giá tối thiểu (VNĐ).",
            },
            "max_price": {
                "type": "integer",
                "description": "Giá tối đa (VNĐ). Dùng khi khách nêu ngân sách.",
            },
            "max_results": {
                "type": "integer",
                "description": "Số sản phẩm tối đa trả về (mặc định 8).",
            },
        },
        "required": [],
    },
}


def build_system_prompt(db: Session) -> str:
    """Tạo system prompt kèm danh sách danh mục thật từ DB."""
    cats = db.query(models.Category).all()
    cat_lines = "\n".join(f"- ID {c.id}: {c.name}" for c in cats)
    return (
        "Bạn là trợ lý tư vấn bán hàng của Bigzone — cửa hàng thương mại điện tử "
        "chuyên PC, laptop, linh kiện và gaming gear. Nhiệm vụ của bạn là tư vấn sản "
        "phẩm phù hợp với nhu cầu và ngân sách của khách hàng.\n\n"
        "Các danh mục sản phẩm hiện có:\n"
        f"{cat_lines}\n\n"
        "QUY TẮC:\n"
        "1. Luôn dùng tool search_products để lấy dữ liệu sản phẩm THẬT trước khi tư vấn. "
        "Tuyệt đối không bịa tên sản phẩm, giá hay thông số.\n"
        "2. Khi khách nêu ngân sách, truyền max_price (và min_price nếu hợp lý) cho tool.\n"
        "3. Khi giới thiệu sản phẩm, nêu rõ TÊN, GIÁ và kèm link dạng Markdown "
        "[tên sản phẩm](/product/ID) để khách bấm xem chi tiết.\n"
        "4. Nếu không tìm thấy sản phẩm phù hợp, nói thật và gợi ý lựa chọn gần nhất.\n"
        "5. Trả lời bằng tiếng Việt, thân thiện, ngắn gọn, đi thẳng vào trọng tâm. "
        "Gợi ý 2-4 sản phẩm là vừa, không liệt kê quá dài.\n"
        "6. Chỉ tư vấn trong phạm vi sản phẩm của Bigzone."
    )


def run_search_products(db: Session, **kwargs) -> str:
    """Thực thi tool: query DB và trả chuỗi JSON kết quả."""
    category_id = kwargs.get("category_id")
    keyword = kwargs.get("keyword")
    min_price = kwargs.get("min_price")
    max_price = kwargs.get("max_price")
    max_results = kwargs.get("max_results") or 8
    max_results = max(1, min(int(max_results), 12))

    query = db.query(models.Product)
    if category_id:
        query = query.filter(models.Product.category_id == category_id)
    if keyword and keyword.strip():
        kw = f"%{keyword.strip()}%"
        query = query.filter(or_(
            models.Product.title.ilike(kw),
            models.Product.brand.ilike(kw),
            models.Product.description.ilike(kw),
        ))
    if min_price:
        query = query.filter(models.Product.price_current >= min_price)
    if max_price:
        query = query.filter(models.Product.price_current <= max_price)

    products = query.order_by(models.Product.price_current.asc()).limit(max_results).all()

    results = []
    for p in products:
        desc = (p.description or "").strip()
        if len(desc) > 160:
            desc = desc[:160] + "..."
        results.append({
            "id": p.id,
            "title": p.title,
            "brand": p.brand,
            "price_current": p.price_current,
            "discount_percent": p.discount_percent,
            "stock": p.stock,
            "category": p.category.name if p.category else None,
            "url": f"/product/{p.id}",
            "description": desc,
        })

    logger.info(
        "search_products(category_id=%s, keyword=%r, min=%s, max=%s) -> %d kết quả",
        category_id, keyword, min_price, max_price, len(results),
    )
    return json.dumps({"count": len(results), "products": results}, ensure_ascii=False)


def _sse(event: str, **data) -> str:
    """Đóng gói một sự kiện SSE."""
    payload = {"type": event, **data}
    return f"data: {json.dumps(payload, ensure_ascii=False)}\n\n"


def stream_chat(messages: list[dict], db: Session):
    """
    Generator đồng bộ: chạy agentic loop (streaming + tool use) và yield các
    sự kiện SSE: delta (text), done, error.
    """
    client = get_client()
    if client is None:
        yield _sse(
            "error",
            message="Chatbot hiện chưa sẵn sàng (thiếu cấu hình API). Vui lòng liên hệ hotline 087.997.9997.",
        )
        yield _sse("done")
        return

    system_prompt = build_system_prompt(db)
    convo = list(messages)  # bản sao để nối thêm các lượt tool

    try:
        for _ in range(MAX_TOOL_ROUNDS):
            with client.messages.stream(
                model=MODEL,
                max_tokens=2048,
                thinking={"type": "adaptive"},
                system=system_prompt,
                tools=[SEARCH_PRODUCTS_TOOL],
                messages=convo,
            ) as stream:
                for text in stream.text_stream:
                    yield _sse("delta", text=text)
                final = stream.get_final_message()

            if final.stop_reason != "tool_use":
                yield _sse("done")
                return

            # Thực thi các tool_use, nối assistant turn + tool_result rồi lặp.
            convo.append({"role": "assistant", "content": final.content})
            tool_results = []
            for block in final.content:
                if block.type == "tool_use":
                    if block.name == "search_products":
                        result = run_search_products(db, **(block.input or {}))
                    else:
                        result = json.dumps({"error": "tool không hỗ trợ"})
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": result,
                    })
            convo.append({"role": "user", "content": tool_results})

        # Vượt quá số vòng tool cho phép
        yield _sse(
            "error",
            message="Xin lỗi, mình cần thêm thời gian để xử lý. Bạn thử hỏi lại cụ thể hơn nhé.",
        )
        yield _sse("done")
    except Exception as e:
        logger.exception("Lỗi khi stream chat: %s", e)
        yield _sse(
            "error",
            message="Đã có lỗi xảy ra khi xử lý. Vui lòng thử lại sau ít phút.",
        )
        yield _sse("done")
