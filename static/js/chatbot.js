/**
 * Bigzone - Chatbot AI tư vấn (streaming + tool use)
 */
document.addEventListener('DOMContentLoaded', () => {
    const chatbot = document.getElementById('chatbot');
    const toggle = document.getElementById('chatbotToggle');
    const panel = document.getElementById('chatbotPanel');
    const messagesEl = document.getElementById('chatbotMessages');
    const form = document.getElementById('chatbotForm');
    const input = document.getElementById('chatbotInput');
    const sendBtn = document.getElementById('chatbotSend');

    if (!chatbot || !toggle || !form) return;

    // Lịch sử hội thoại gửi lên API (stateless ở server).
    const history = [];
    let busy = false;

    // ── HTML escape (chống XSS) ───────────────────────────────────────────
    const esc = (str) => {
        const div = document.createElement('div');
        div.appendChild(document.createTextNode(str ?? ''));
        return div.innerHTML;
    };

    // Escape trước, rồi linkify [text](url) và xuống dòng. Chỉ cho phép link nội bộ.
    const renderText = (text) => {
        let html = esc(text);
        html = html.replace(/\[([^\]]+)\]\((\/[^\s)]*)\)/g,
            (_m, label, url) => `<a href="${url}">${label}</a>`);
        return html.replace(/\n/g, '<br>');
    };

    // ── Mở/đóng panel ─────────────────────────────────────────────────────
    const openPanel = () => {
        chatbot.classList.add('open');
        panel.setAttribute('aria-hidden', 'false');
        setTimeout(() => input.focus(), 250);
    };
    const closePanel = () => {
        chatbot.classList.remove('open');
        panel.setAttribute('aria-hidden', 'true');
    };
    toggle.addEventListener('click', () => {
        chatbot.classList.contains('open') ? closePanel() : openPanel();
    });

    // ── Helpers dựng tin nhắn ─────────────────────────────────────────────
    const scrollToBottom = () => { messagesEl.scrollTop = messagesEl.scrollHeight; };

    const addMessage = (role, text) => {
        const wrap = document.createElement('div');
        wrap.className = `chat-msg chat-msg-${role === 'user' ? 'user' : 'bot'}`;
        const bubble = document.createElement('div');
        bubble.className = 'chat-bubble';
        bubble.innerHTML = role === 'user' ? esc(text) : renderText(text);
        wrap.appendChild(bubble);
        messagesEl.appendChild(wrap);
        scrollToBottom();
        return bubble;
    };

    const addTyping = () => {
        const wrap = document.createElement('div');
        wrap.className = 'chat-msg chat-msg-bot';
        wrap.innerHTML = `<div class="chat-bubble"><span class="chat-typing">
            <span></span><span></span><span></span></span></div>`;
        messagesEl.appendChild(wrap);
        scrollToBottom();
        return wrap;
    };

    // ── Gửi tin nhắn ──────────────────────────────────────────────────────
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        const text = input.value.trim();
        if (!text || busy) return;

        busy = true;
        input.value = '';
        sendBtn.disabled = true;

        addMessage('user', text);
        history.push({ role: 'user', content: text });

        const typingEl = addTyping();
        let bubble = null;       // bong bóng bot khi bắt đầu có text
        let answer = '';

        try {
            const res = await fetch('/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ messages: history }),
            });

            if (!res.ok || !res.body) throw new Error('network');

            const reader = res.body.getReader();
            const decoder = new TextDecoder();
            let buffer = '';

            const handleEvent = (payload) => {
                if (payload.type === 'delta') {
                    if (!bubble) {
                        typingEl.remove();
                        bubble = addMessage('bot', '');
                    }
                    answer += payload.text;
                    bubble.innerHTML = renderText(answer);
                    scrollToBottom();
                } else if (payload.type === 'error') {
                    if (!bubble) { typingEl.remove(); bubble = addMessage('bot', ''); }
                    answer = payload.message;
                    bubble.innerHTML = renderText(answer);
                    scrollToBottom();
                }
            };

            // Đọc SSE stream
            while (true) {
                const { done, value } = await reader.read();
                if (done) break;
                buffer += decoder.decode(value, { stream: true });
                const parts = buffer.split('\n\n');
                buffer = parts.pop();   // phần dở dang
                for (const part of parts) {
                    const line = part.trim();
                    if (!line.startsWith('data:')) continue;
                    try {
                        handleEvent(JSON.parse(line.slice(5).trim()));
                    } catch { /* bỏ qua chunk lỗi */ }
                }
            }

            if (typingEl.isConnected) typingEl.remove();
            if (answer) history.push({ role: 'assistant', content: answer });
        } catch {
            if (typingEl.isConnected) typingEl.remove();
            addMessage('bot', 'Xin lỗi, không kết nối được tới máy chủ. Vui lòng thử lại.');
            window.showToast?.('Không kết nối được tới chatbot', 'error');
        } finally {
            busy = false;
            sendBtn.disabled = false;
            input.focus();
        }
    });
});
