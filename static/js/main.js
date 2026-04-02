/**
 * Bigzone - Main JavaScript
 */
document.addEventListener('DOMContentLoaded', () => {

    // ── HTML escape helper (chống XSS) ─────────────────────────────────────
    const esc = (str) => {
        const div = document.createElement('div');
        div.appendChild(document.createTextNode(str ?? ''));
        return div.innerHTML;
    };

    const fmt = (n) => Number(n).toLocaleString('vi-VN') + ' VNĐ';

    // ── Toast Notification System ────────────────────────────────────────────
    let toastContainer = document.querySelector('.toast-container');
    if (!toastContainer) {
        toastContainer = document.createElement('div');
        toastContainer.className = 'toast-container';
        document.body.appendChild(toastContainer);
    }

    function showToast(message, type = 'info', duration = 3000) {
        const icons = {
            success: 'ph-fill ph-check-circle',
            error: 'ph-fill ph-warning-circle',
            info: 'ph-fill ph-info',
        };
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        toast.innerHTML = `
            <i class="${icons[type] || icons.info}"></i>
            <span>${esc(message)}</span>
            <button class="toast-close"><i class="ph-bold ph-x"></i></button>
        `;
        toastContainer.appendChild(toast);

        const close = () => {
            toast.classList.add('toast-out');
            setTimeout(() => toast.remove(), 300);
        };

        toast.querySelector('.toast-close').addEventListener('click', close);
        setTimeout(close, duration);
    }
    window.showToast = showToast;

    // ── Scroll effects ──────────────────────────────────────────────────────
    const scrollToTopBtn = document.getElementById('scrollToTop');
    const header = document.getElementById('header');

    if (header) {
        window.addEventListener('scroll', () => {
            if (scrollToTopBtn) {
                scrollToTopBtn.classList.toggle('visible', window.scrollY > 300);
            }
            if (window.scrollY > 50) {
                header.style.boxShadow = 'var(--shadow-lg)';
                header.style.backdropFilter = 'blur(10px)';
            } else {
                header.style.boxShadow = 'var(--shadow-md)';
                header.style.backdropFilter = 'none';
            }
        });
    }

    if (scrollToTopBtn) {
        scrollToTopBtn.addEventListener('click', () => {
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });
    }

    // ── Mobile Menu ──────────────────────────────────────────────────────────
    const mobileToggle = document.getElementById('mobileMenuToggle');
    const mobileToggle2 = document.getElementById('mobileMenuToggle2');
    const mobileMenu = document.getElementById('mobileMenu');
    const mobileOverlay = document.getElementById('mobileOverlay');

    const closeMobileMenu = () => {
        mobileMenu?.classList.remove('open');
        mobileOverlay?.classList.remove('open');
        document.body.style.overflow = '';
    };

    if (mobileToggle && mobileMenu) {
        mobileToggle.addEventListener('click', () => {
            mobileMenu.classList.toggle('open');
            mobileOverlay?.classList.toggle('open');
            document.body.style.overflow = mobileMenu.classList.contains('open') ? 'hidden' : '';
        });

        mobileToggle2?.addEventListener('click', closeMobileMenu);
        mobileOverlay?.addEventListener('click', closeMobileMenu);

        // Close on link click
        mobileMenu.querySelectorAll('a').forEach(a => {
            a.addEventListener('click', () => {
                mobileMenu.classList.remove('open');
                mobileOverlay?.classList.remove('open');
                document.body.style.overflow = '';
            });
        });
    }

    // ── Cart helpers ────────────────────────────────────────────────────────
    let cart = JSON.parse(localStorage.getItem('bigzone_cart')) || [];

    const saveCart = () => {
        localStorage.setItem('bigzone_cart', JSON.stringify(cart));
        updateCartCount();
    };

    const updateCartCount = () => {
        const total = cart.reduce((sum, item) => sum + item.quantity, 0);
        document.querySelectorAll('.cart-count').forEach(el => el.textContent = total);
    };

    function addToCart(id, title, price, quantity = 1, image = '') {
        const existing = cart.find(i => i.id == id);
        if (existing) {
            existing.quantity += quantity;
            if (image && !existing.image) existing.image = image;
        } else {
            cart.push({ id, title, price, quantity, image });
        }
        saveCart();
        showToast(`Đã thêm "${title}" vào giỏ hàng`, 'success');
    }
    window.addToCart = addToCart;

    // ── Add to cart from product cards ─────────────────────────────────────
    document.querySelectorAll('.btn-cart-add').forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            e.stopPropagation();

            const card = e.currentTarget.closest('.product-card');
            if (!card) return;

            const id = card.dataset.id || String(Math.random());
            const title = card.dataset.title || card.querySelector('.product-name')?.textContent || '';
            const price = parseInt(card.dataset.price) || 0;
            const img = card.querySelector('.product-image img');
            const image = img ? img.src : '';

            addToCart(id, title, price, 1, image);

            // Visual feedback
            btn.innerHTML = '<i class="ph-fill ph-check"></i>';
            setTimeout(() => { btn.innerHTML = '<i class="ph-bold ph-shopping-cart"></i>'; }, 1500);
        });
    });

    // ── Navigate to product page on card click ──────────────────────────────
    document.querySelectorAll('.product-card').forEach(card => {
        card.style.cursor = 'pointer';
        card.addEventListener('click', (e) => {
            if (e.target.closest('.btn-cart-add')) return;
            if (e.target.closest('a')) return;
            const id = card.dataset.id;
            if (id) window.location.href = `/product/${id}`;
        });
    });

    // ── Cart page ───────────────────────────────────────────────────────────
    if (window.location.pathname === '/cart') {
        const container = document.getElementById('cartContainer');
        const layout = document.getElementById('cartLayout');
        const empty = document.getElementById('cartEmpty');
        const totalText = document.getElementById('cartTotalText');
        const subtotalText = document.getElementById('cartSubtotal');
        const itemCountEl = document.getElementById('cartItemCount');

        const renderCartPage = () => {
            if (!container) return;
            if (cart.length === 0) {
                container.innerHTML = '';
                if (layout) layout.style.display = 'none';
                if (empty) empty.style.display = 'block';
                return;
            }
            if (empty) empty.style.display = 'none';
            if (layout) layout.style.display = 'grid';

            let html = '';
            let total = 0;
            let itemCount = 0;
            cart.forEach((item, index) => {
                const lineTotal = Number(item.price) * Number(item.quantity);
                total += lineTotal;
                itemCount += Number(item.quantity);
                html += `
                    <div class="cart-item">
                        <div class="cart-item-img">
                            ${item.image
                                ? `<img src="${esc(item.image)}" alt="${esc(item.title)}">`
                                : `<i class="ph-fill ph-image img-placeholder"></i>`
                            }
                        </div>
                        <div class="cart-item-info">
                            <h3><a href="/product/${esc(String(item.id))}">${esc(item.title)}</a></h3>
                            <span class="cart-item-price">${fmt(item.price)}</span>
                        </div>
                        <div class="cart-item-qty">
                            <button class="qty-btn" onclick="updateQty(${index}, -1)">-</button>
                            <span class="qty-display">${item.quantity}</span>
                            <button class="qty-btn" onclick="updateQty(${index}, 1)">+</button>
                        </div>
                        <div class="cart-item-total">${fmt(lineTotal)}</div>
                        <button class="remove-btn" onclick="removeItem(${index})" title="Xoá sản phẩm">
                            <i class="ph-bold ph-trash"></i>
                        </button>
                    </div>`;
            });
            container.innerHTML = html;
            if (totalText) totalText.textContent = fmt(total);
            if (subtotalText) subtotalText.textContent = fmt(total);
            if (itemCountEl) itemCountEl.textContent = itemCount;
        };

        window.updateQty = (index, delta) => {
            cart[index].quantity += delta;
            if (cart[index].quantity <= 0) {
                cart.splice(index, 1);
                showToast('Đã xoá sản phẩm khỏi giỏ hàng', 'info');
            }
            saveCart();
            renderCartPage();
        };

        window.removeItem = (index) => {
            const name = cart[index]?.title || 'Sản phẩm';
            cart.splice(index, 1);
            saveCart();
            renderCartPage();
            showToast(`Đã xoá "${name}" khỏi giỏ hàng`, 'info');
        };

        document.getElementById('btnClearCart')?.addEventListener('click', () => {
            if (cart.length === 0) return;
            cart = [];
            saveCart();
            renderCartPage();
            showToast('Đã xoá toàn bộ giỏ hàng', 'info');
        });

        renderCartPage();

        document.getElementById('btnGoToCheckout')?.addEventListener('click', () => {
            if (cart.length === 0) {
                showToast('Giỏ hàng trống!', 'error');
                return;
            }
            window.location.href = '/checkout';
        });
    }

    // ── Checkout page ───────────────────────────────────────────────────────
    if (window.location.pathname === '/checkout') {
        const orderItemsList = document.getElementById('checkoutOrderItems');
        const subtotalEl = document.getElementById('checkoutSubtotal');
        const totalEl = document.getElementById('checkoutTotal');
        const checkoutForm = document.getElementById('checkoutForm');
        const checkoutEmpty = document.getElementById('checkoutEmpty');
        const bankInfo = document.getElementById('bankInfo');

        // Redirect if cart empty
        if (cart.length === 0) {
            if (checkoutForm) checkoutForm.style.display = 'none';
            if (checkoutEmpty) checkoutEmpty.style.display = 'block';
        } else {
            if (checkoutForm) checkoutForm.style.display = 'grid';
            if (checkoutEmpty) checkoutEmpty.style.display = 'none';
        }

        // Render order summary
        if (orderItemsList && cart.length > 0) {
            let total = 0;
            cart.forEach(item => {
                const lineTotal = Number(item.price) * Number(item.quantity);
                total += lineTotal;
                orderItemsList.innerHTML += `
                    <div class="checkout-item">
                        <span class="checkout-item-qty">x${Number(item.quantity)}</span>
                        <span class="checkout-item-title">${esc(item.title)}</span>
                        <span class="checkout-item-price">${fmt(lineTotal)}</span>
                    </div>`;
            });
            if (subtotalEl) subtotalEl.textContent = fmt(total);
            if (totalEl) totalEl.textContent = fmt(total);
        }

        // Toggle bank info
        document.querySelectorAll('input[name="payment"]').forEach(radio => {
            radio.addEventListener('change', () => {
                if (bankInfo) {
                    bankInfo.style.display = radio.value === 'bank' && radio.checked ? 'block' : 'none';
                }
            });
        });

        // Form validation
        function validateCheckoutForm(form) {
            let isValid = true;
            // Clear previous errors
            form.querySelectorAll('.error').forEach(el => el.classList.remove('error'));
            form.querySelectorAll('.error-msg').forEach(el => el.remove());

            const addError = (input, msg) => {
                isValid = false;
                input.classList.add('error');
                const err = document.createElement('span');
                err.className = 'error-msg';
                err.textContent = msg;
                input.parentNode.appendChild(err);
            };

            const name = form.querySelector('[name="name"]');
            if (!name.value.trim()) addError(name, 'Vui lòng nhập họ tên');

            const phone = form.querySelector('[name="phone"]');
            const phoneVal = phone.value.trim();
            if (!phoneVal) {
                addError(phone, 'Vui lòng nhập số điện thoại');
            } else if (!/^(0|\+84)[0-9]{8,10}$/.test(phoneVal.replace(/[\s.-]/g, ''))) {
                addError(phone, 'Số điện thoại không hợp lệ');
            }

            const email = form.querySelector('[name="email"]');
            if (email.value.trim() && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value.trim())) {
                addError(email, 'Email không hợp lệ');
            }

            const province = form.querySelector('[name="province"]');
            if (province && !province.value) addError(province, 'Vui lòng chọn tỉnh/thành phố');

            const district = form.querySelector('[name="district"]');
            if (district && !district.value.trim()) addError(district, 'Vui lòng nhập quận/huyện');

            const address = form.querySelector('[name="address"]');
            if (!address.value.trim()) addError(address, 'Vui lòng nhập địa chỉ');

            // Scroll to first error
            if (!isValid) {
                const firstError = form.querySelector('.error');
                if (firstError) firstError.scrollIntoView({ behavior: 'smooth', block: 'center' });
            }

            return isValid;
        }

        // Submit order
        checkoutForm?.addEventListener('submit', async (e) => {
            e.preventDefault();

            if (!validateCheckoutForm(checkoutForm)) return;

            const submitBtn = document.getElementById('btnSubmitOrder');
            if (submitBtn) {
                submitBtn.classList.add('btn-loading');
                submitBtn.disabled = true;
                submitBtn.innerHTML = '<i class="ph-bold ph-spinner"></i> Đang xử lý...';
            }

            const formData = new FormData(e.target);
            const province = formData.get('province') || '';
            const district = formData.get('district') || '';
            const streetAddress = formData.get('address') || '';
            const fullAddress = [streetAddress, district, province].filter(Boolean).join(', ');

            const orderData = {
                customer: {
                    name: formData.get('name'),
                    phone: formData.get('phone'),
                    email: formData.get('email') || '',
                    address: fullAddress,
                    note: formData.get('note') || '',
                    payment: formData.get('payment') || 'cod',
                },
                items: cart,
                total: cart.reduce((sum, item) => sum + item.price * item.quantity, 0),
            };

            try {
                const res = await fetch('/api/orders', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(orderData),
                });

                const data = await res.json();

                if (res.ok && data.status === 'success') {
                    localStorage.removeItem('bigzone_cart');
                    cart = [];
                    updateCartCount();
                    window.location.href = `/order-success/${data.order_id}`;
                } else {
                    const msg = data.detail || 'Có lỗi xảy ra khi đặt hàng.';
                    showToast(msg, 'error', 5000);
                }
            } catch {
                showToast('Không thể kết nối đến server. Vui lòng thử lại.', 'error', 5000);
            } finally {
                if (submitBtn) {
                    submitBtn.classList.remove('btn-loading');
                    submitBtn.disabled = false;
                    submitBtn.innerHTML = '<i class="ph-bold ph-seal-check"></i> HOÀN TẤT ĐẶT HÀNG';
                }
            }
        });

        // Clear validation on input
        checkoutForm?.querySelectorAll('input, textarea, select').forEach(input => {
            input.addEventListener('input', () => {
                input.classList.remove('error');
                const msg = input.parentNode.querySelector('.error-msg');
                if (msg) msg.remove();
            });
        });
    }

    // ── Newsletter form ─────────────────────────────────────────────────────
    const newsletterBtn = document.querySelector('.newsletter-form .btn');
    if (newsletterBtn) {
        newsletterBtn.addEventListener('click', (e) => {
            e.preventDefault();
            const input = document.querySelector('.newsletter-form input');
            if (!input || !input.value.trim()) {
                showToast('Vui lòng nhập email', 'error');
                return;
            }
            if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(input.value.trim())) {
                showToast('Email không hợp lệ', 'error');
                return;
            }
            showToast('Đăng ký nhận tin thành công!', 'success');
            input.value = '';
        });
    }

    updateCartCount();
});
