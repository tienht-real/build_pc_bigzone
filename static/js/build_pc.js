/*
 * Bigzone - Trang Build PC: chọn linh kiện, tính tổng, thêm cả bộ vào giỏ.
 */
(function () {
    if (window.location.pathname !== '/build-pc') return;

    document.addEventListener('DOMContentLoaded', function () {
        const selections = {};          // { slotKey: {id, title, price, image} }
        const totalSlots = document.querySelectorAll('.build-slot').length;

        const fmt = (n) => new Intl.NumberFormat('vi-VN').format(n) + ' VNĐ';

        const totalEl = document.getElementById('buildTotal');
        const countEl = document.getElementById('buildCount');
        const btnAdd = document.getElementById('btnAddBuild');
        const btnReset = document.getElementById('btnResetBuild');

        function openModal(slot) {
            const m = document.getElementById('modal-' + slot);
            if (m) m.classList.add('open');
        }
        function closeModal(slot) {
            const m = document.getElementById('modal-' + slot);
            if (m) m.classList.remove('open');
        }

        // Mở modal
        document.querySelectorAll('.btn-pick').forEach(btn => {
            btn.addEventListener('click', () => openModal(btn.dataset.slot));
        });
        // Đóng modal (nút X)
        document.querySelectorAll('.modal-close').forEach(btn => {
            btn.addEventListener('click', () => closeModal(btn.dataset.slot));
        });
        // Đóng modal khi bấm nền tối
        document.querySelectorAll('.build-modal').forEach(m => {
            m.addEventListener('click', (e) => { if (e.target === m) m.classList.remove('open'); });
        });

        // Chọn 1 linh kiện trong modal
        document.querySelectorAll('.pick-item .btn-pick-confirm').forEach(btn => {
            btn.addEventListener('click', () => {
                const item = btn.closest('.pick-item');
                const slot = item.dataset.slot;
                selections[slot] = {
                    id: item.dataset.id,
                    title: item.dataset.title,
                    price: parseInt(item.dataset.price, 10),
                    image: item.dataset.image,
                };
                renderSlot(slot);
                closeModal(slot);
                recompute();
            });
        });

        // Xoá lựa chọn
        document.querySelectorAll('.btn-remove').forEach(btn => {
            btn.addEventListener('click', () => {
                const slot = btn.dataset.slot;
                delete selections[slot];
                renderSlot(slot);
                recompute();
            });
        });

        function renderSlot(slot) {
            const row = document.querySelector('.build-slot[data-slot="' + slot + '"]');
            if (!row) return;
            const empty = row.querySelector('.slot-empty');
            const sel = row.querySelector('.slot-selected');
            const pickBtn = row.querySelector('.btn-pick');
            const removeBtn = row.querySelector('.btn-remove');
            const data = selections[slot];

            if (data) {
                empty.style.display = 'none';
                sel.style.display = 'flex';
                sel.querySelector('.sel-img').src = data.image;
                sel.querySelector('.sel-title').textContent = data.title;
                sel.querySelector('.sel-price').textContent = fmt(data.price);
                if (pickBtn) pickBtn.innerHTML = '<i class="ph-bold ph-arrows-clockwise"></i> Đổi';
                if (removeBtn) removeBtn.style.display = 'inline-flex';
            } else {
                empty.style.display = 'block';
                sel.style.display = 'none';
                if (pickBtn) pickBtn.innerHTML = '<i class="ph-bold ph-plus-circle"></i> Chọn';
                if (removeBtn) removeBtn.style.display = 'none';
            }
        }

        function recompute() {
            const keys = Object.keys(selections);
            const total = keys.reduce((s, k) => s + selections[k].price, 0);
            totalEl.textContent = fmt(total);
            countEl.textContent = keys.length + ' / ' + totalSlots;
            btnAdd.disabled = keys.length === 0;
        }

        // Thêm cả bộ vào giỏ
        btnAdd.addEventListener('click', () => {
            const keys = Object.keys(selections);
            if (keys.length === 0) return;
            if (typeof window.addToCart !== 'function') {
                alert('Không thêm được vào giỏ. Vui lòng tải lại trang.');
                return;
            }
            keys.forEach(k => {
                const d = selections[k];
                window.addToCart(d.id, d.title, d.price, 1, d.image);
            });
            window.location.href = '/cart';
        });

        // Làm lại
        btnReset.addEventListener('click', () => {
            Object.keys(selections).forEach(k => delete selections[k]);
            document.querySelectorAll('.build-slot').forEach(r => renderSlot(r.dataset.slot));
            recompute();
        });

        recompute();
    });
})();
