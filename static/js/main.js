// Proje scriptleri

// Bildirim sayısını güncelle
function updateNotificationBadge() {
    const badge = document.getElementById('notification-badge');
    if (!badge) return;

    fetch('/bildirimler/ajax/sayac/')
        .then((response) => response.json())
        .then((data) => {
            if (data.unread_count > 0) {
                badge.textContent = data.unread_count;
                badge.style.display = 'inline';
            } else {
                badge.style.display = 'none';
            }
        })
        .catch(() => {
            // Sessizce yut
        });
}

// Bildirim listesini getir
function loadNotifications() {
    const listDiv = document.getElementById('notification-list');
    if (!listDiv) return;

    fetch('/bildirimler/ajax/son-bildirimler/')
        .then((response) => response.json())
        .then((data) => {
            if (!data.notifications || data.notifications.length === 0) {
                listDiv.innerHTML =
                    '<li><span class="dropdown-item-text text-muted">Bildirim yok</span></li>';
                return;
            }
            let html = '';
            data.notifications.forEach((n) => {
                const link = n.link || '#';
                const messagePreview =
                    (n.message || '').length > 40
                        ? n.message.substring(0, 40) + '...'
                        : n.message || '';
                html += `
                    <li>
                        <a class="dropdown-item ${n.is_read ? '' : 'fw-bold'}" href="${link}">
                            <div class="d-flex flex-column">
                                <span>${n.title}</span>
                                <small class="text-muted">${messagePreview}</small>
                                <small class="text-muted">${n.created_at}</small>
                            </div>
                        </a>
                    </li>
                `;
            });
            listDiv.innerHTML = html;
        })
        .catch(() => {
            listDiv.innerHTML =
                '<li><span class="dropdown-item-text text-muted">Bildirimler yüklenemedi</span></li>';
        });
}

document.addEventListener('DOMContentLoaded', function () {
    // Sayfa yüklendiğinde ve periyodik olarak bildirim sayısını güncelle
    updateNotificationBadge();
    setInterval(updateNotificationBadge, 30000); // her 30 saniyede bir

    // Dropdown açıldığında bildirimleri yükle
    const dropdown = document.getElementById('notificationDropdown');
    if (dropdown) {
        dropdown.addEventListener('show.bs.dropdown', function () {
            loadNotifications();
        });
    }
});

