"""
Chatbot AI tư vấn sản phẩm cho Bigzone.

Dùng model của NVIDIA (qua OpenAI SDK, endpoint integrate.api.nvidia.com) với
function calling để truy vấn dữ liệu sản phẩm thật trong CSDL, và stream câu
trả lời về client qua SSE.
"""
import json
import logging
import os
import time

from sqlalchemy import or_
from sqlalchemy.orm import Session

import models

logger = logging.getLogger("bigzone.chatbot")

# Cấu hình qua biến môi trường (có giá trị mặc định cho NVIDIA NIM).
BASE_URL = os.environ.get("NVIDIA_BASE_URL", "https://integrate.api.nvidia.com/v1")
MODEL = os.environ.get("NVIDIA_MODEL", "nvidia/nemotron-3-ultra-550b-a55b")
MAX_TOOL_ROUNDS = 5

# ⚠️ TẠM HARDCODE KEY — NHỚ XÓA và rotate key sau khi test xong.
# Ưu tiên biến môi trường NVIDIA_API_KEY; nếu không có thì dùng key dưới đây.
_FALLBACK_API_KEY = "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"

# Retry khi NVIDIA báo quá tải tạm thời (ResourceExhausted / 429 / 503 ...).
MAX_RETRIES = 4
RETRY_BASE_DELAY = 2  # giây; lần thử thứ n đợi RETRY_BASE_DELAY * n


def _is_retryable(err: Exception) -> bool:
    """Đúng nếu lỗi là dạng quá tải tạm thời, nên thử lại."""
    msg = str(err).lower()
    return any(k in msg for k in (
        "resourceexhausted", "request limit", "worker local",
        "429", "too many requests", "503", "overloaded", "unavailable",
    ))

# Lazy import + khởi tạo client để web vẫn chạy được khi chưa cài/đặt key.
_client = None
_client_ready = False


def get_client():
    """Trả về OpenAI client trỏ tới NVIDIA, hoặc None nếu thiếu key / chưa cài SDK."""
    global _client, _client_ready
    if _client_ready:
        return _client
    _client_ready = True
    api_key = os.environ.get("NVIDIA_API_KEY") or _FALLBACK_API_KEY
    if not api_key:
        logger.warning("Thiếu NVIDIA_API_KEY — chatbot bị tắt.")
        _client = None
        return None
    try:
        from openai import OpenAI
        _client = OpenAI(base_url=BASE_URL, api_key=api_key)
    except Exception as e:  # SDK chưa cài hoặc lỗi khởi tạo
        logger.warning("Không khởi tạo được OpenAI/NVIDIA client: %s", e)
        _client = None
    return _client


# ── Định nghĩa tool tìm sản phẩm (chuẩn OpenAI function calling) ──────────────
SEARCH_PRODUCTS_TOOL = {
    "type": "function",
    "function": {
        "name": "search_products",
        "description": (
            "Tìm sản phẩm trong cửa hàng Bigzone theo danh mục, từ khoá và khoảng giá. "
            "Luôn dùng tool này để lấy dữ liệu sản phẩm THẬT trước khi tư vấn — "
            "không được tự bịa ra sản phẩm, giá hay thông số."
        ),
        "parameters": {
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
    Generator đồng bộ: chạy agentic loop (streaming + function calling) và yield
    các sự kiện SSE: delta (text), done, error.
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
    # OpenAI/NVIDIA: system prompt là message role="system" ở đầu hội thoại.
    convo = [{"role": "system", "content": system_prompt}] + list(messages)

    try:
        for _ in range(MAX_TOOL_ROUNDS):
            # Mỗi vòng tool: thử lại khi NVIDIA quá tải, nhưng CHỈ khi chưa
            # stream chữ nào ra cho khách (nếu đã stream thì retry sẽ lặp text).
            attempt = 0
            while True:
                content_parts = []
                tool_calls = {}  # index -> {"id", "name", "arguments"}
                finish_reason = None
                emitted = False
                try:
                    stream = client.chat.completions.create(
                        model=MODEL,
                        messages=convo,
                        tools=[SEARCH_PRODUCTS_TOOL],
                        temperature=1,
                        top_p=0.95,
                        max_tokens=16384,
                        extra_body={"chat_template_kwargs": {"enable_thinking": True}},
                        stream=True,
                    )

                    for chunk in stream:
                        if not chunk.choices:
                            continue
                        choice = chunk.choices[0]
                        delta = choice.delta
                        if choice.finish_reason:
                            finish_reason = choice.finish_reason

                        # Phần trả lời cho khách → stream về client.
                        text = getattr(delta, "content", None)
                        if text:
                            content_parts.append(text)
                            emitted = True
                            yield _sse("delta", text=text)

                        # Phần reasoning của model → bỏ qua, không hiển thị cho khách.

                        # Tích luỹ các tool_call (đến theo từng mảnh).
                        for tc in (getattr(delta, "tool_calls", None) or []):
                            slot = tool_calls.setdefault(
                                tc.index, {"id": "", "name": "", "arguments": ""}
                            )
                            if tc.id:
                                slot["id"] = tc.id
                            if tc.function and tc.function.name:
                                slot["name"] = tc.function.name
                            if tc.function and tc.function.arguments:
                                slot["arguments"] += tc.function.arguments
                    break  # vòng stream thành công → thoát retry loop
                except Exception as e:
                    if _is_retryable(e) and not emitted and attempt < MAX_RETRIES:
                        attempt += 1
                        delay = RETRY_BASE_DELAY * attempt
                        logger.warning(
                            "NVIDIA quá tải (%s) — thử lại lần %d/%d sau %ds.",
                            e, attempt, MAX_RETRIES, delay,
                        )
                        yield _sse("status", message="Hệ thống đang bận, đang thử lại…")
                        time.sleep(delay)
                        continue
                    raise  # không retry được → để outer except xử lý

            # Không gọi tool → đã có câu trả lời cuối cùng.
            if not tool_calls:
                yield _sse("done")
                return

            # Nối assistant turn (kèm tool_calls) + kết quả tool rồi lặp lại.
            convo.append({
                "role": "assistant",
                "content": "".join(content_parts) or None,
                "tool_calls": [
                    {
                        "id": s["id"],
                        "type": "function",
                        "function": {"name": s["name"], "arguments": s["arguments"] or "{}"},
                    }
                    for s in tool_calls.values()
                ],
            })

            for s in tool_calls.values():
                try:
                    args = json.loads(s["arguments"] or "{}")
                except json.JSONDecodeError:
                    args = {}
                if s["name"] == "search_products":
                    result = run_search_products(db, **args)
                else:
                    result = json.dumps({"error": "tool không hỗ trợ"})
                convo.append({
                    "role": "tool",
                    "tool_call_id": s["id"],
                    "content": result,
                })

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
