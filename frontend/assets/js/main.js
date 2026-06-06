/* ═══════════════════════════════════════════════
   CONECTIO — Main Application Logic
   Page-specific initialization and shared utilities
   ═══════════════════════════════════════════════ */

document.addEventListener('DOMContentLoaded', () => {
    // Render dynamic navbar based on auth state
    renderNavbar();

    // Setup mobile menu toggle
    setupMobileMenu();

    // Setup dropdown menus
    setupDropdowns();

    // Setup notification bell
    setupNotificationBell();
});


/* ── Dynamic Navbar ────────────────────────── */

/**
 * Renders the correct navbar HTML based on auth state.
 * Called on every page's DOMContentLoaded.
 */
function renderNavbar() {
    const navLinks = document.getElementById('navbar-links');
    if (!navLinks) return;

    const loggedIn = window.auth && window.auth.isLoggedIn();
    const user = loggedIn ? window.auth.getCurrentUser() : null;

    // Detect current page for active state
    const currentPage = window.location.pathname.split('/').pop() || 'index.html';

    if (loggedIn && user) {
        const displayName = user.first_name || user.username || 'Me';
        const initial = displayName.charAt(0).toUpperCase();
        const unreadCount = getUnreadNotificationCount();

        navLinks.innerHTML = `
            <a href="index.html" class="navbar__link ${currentPage === 'index.html' ? 'navbar__link--active' : ''}" id="nav-home">
                <span class="navbar__link-icon">🏠</span>
                <span class="navbar__link-label">Home</span>
            </a>
            <a href="profile.html" class="navbar__link ${currentPage === 'profile.html' ? 'navbar__link--active' : ''}" id="nav-network">
                <span class="navbar__link-icon">👥</span>
                <span class="navbar__link-label">My Network</span>
            </a>
            <a href="explore.html" class="navbar__link ${currentPage === 'explore.html' ? 'navbar__link--active' : ''}" id="nav-explore">
                <span class="navbar__link-icon">🔍</span>
                <span class="navbar__link-label">Explore</span>
            </a>

            <!-- Notification Bell -->
            <div class="navbar__link notification-bell" id="notification-bell" tabindex="0" role="button" aria-label="Notifications">
                <span class="navbar__link-icon">🔔</span>
                <span class="navbar__link-label">Alerts</span>
                ${unreadCount > 0 ? '<span class="notification-dot" id="notification-dot"></span>' : ''}
                <div class="notification-dropdown" id="notification-dropdown">
                    <div class="notification-dropdown__header">
                        Notifications
                        <button class="notification-dropdown__clear" id="notification-clear-btn">Clear all</button>
                    </div>
                    <div class="notification-dropdown__list" id="notification-list"></div>
                </div>
            </div>

            <!-- User menu -->
            <div class="dropdown" id="nav-user-dropdown">
                <button class="navbar__link" data-dropdown aria-label="User menu" id="nav-menu-btn">
                    <span class="navbar__avatar-mini" style="
                        width: 24px; height: 24px;
                        border-radius: 50%;
                        background: var(--color-primary-light);
                        color: var(--color-primary);
                        display: flex; align-items: center; justify-content: center;
                        font-size: 12px; font-weight: 700;
                    ">${initial}</span>
                    <span class="navbar__link-label">Me ▾</span>
                </button>
                <div class="dropdown__menu">
                    <div style="padding: 12px 16px; border-bottom: 1px solid var(--color-border);">
                        <div style="font-weight: 600; font-size: 14px;">${displayName}</div>
                        <div style="font-size: 12px; color: var(--color-text-secondary); margin-top: 2px;">
                            ${user.headline || user.email || '@' + user.username}
                        </div>
                    </div>
                    <a href="profile.html" class="dropdown__item" id="dropdown-profile">
                        👤 View Profile
                    </a>
                    <hr class="dropdown__divider">
                    <button class="dropdown__item" id="dropdown-logout" style="color: var(--color-error);">
                        🚪 Sign Out
                    </button>
                </div>
            </div>
        `;

        // Bind logout
        const logoutBtn = document.getElementById('dropdown-logout');
        if (logoutBtn) {
            logoutBtn.addEventListener('click', () => window.auth.logout());
        }

    } else {
        navLinks.innerHTML = `
            <a href="index.html" class="navbar__link ${currentPage === 'index.html' ? 'navbar__link--active' : ''}" id="nav-home">
                <span class="navbar__link-icon">🏠</span>
                <span class="navbar__link-label">Home</span>
            </a>
            <a href="explore.html" class="navbar__link ${currentPage === 'explore.html' ? 'navbar__link--active' : ''}" id="nav-explore">
                <span class="navbar__link-icon">🔍</span>
                <span class="navbar__link-label">Explore</span>
            </a>

            <div id="nav-auth" style="display: flex; align-items: center; gap: 4px;">
                <a href="login.html" class="navbar__link" id="nav-signin">
                    <span class="navbar__link-icon">👤</span>
                    <span class="navbar__link-label">Sign In</span>
                </a>
                <a href="register.html" class="btn-primary btn-primary--sm navbar__cta" id="nav-join">
                    Join now
                </a>
            </div>
        `;
    }
}


/* ── Mobile Menu ───────────────────────────── */
function setupMobileMenu() {
    const toggle = document.getElementById('mobile-menu-toggle');
    const nav = document.getElementById('navbar-links');

    if (!toggle || !nav) return;

    toggle.addEventListener('click', () => {
        nav.classList.toggle('navbar__links--open');
        toggle.setAttribute(
            'aria-expanded',
            nav.classList.contains('navbar__links--open')
        );
    });
}


/* ── Dropdown Menus ────────────────────────── */
function setupDropdowns() {
    document.addEventListener('click', (e) => {
        // Close all open dropdowns
        document.querySelectorAll('.dropdown--open').forEach(dd => {
            if (!dd.contains(e.target)) {
                dd.classList.remove('dropdown--open');
            }
        });

        // Toggle clicked dropdown
        const trigger = e.target.closest('[data-dropdown]');
        if (trigger) {
            const dropdown = trigger.closest('.dropdown');
            if (dropdown) {
                dropdown.classList.toggle('dropdown--open');
            }
        }
    });
}


/* ── Toast Notifications ───────────────────── */
function showToast(message, type = 'success', duration = 3000) {
    // Create toast container if it doesn't exist
    let container = document.getElementById('toast-container');
    if (!container) {
        container = document.createElement('div');
        container.id = 'toast-container';
        container.style.cssText = `
            position: fixed;
            bottom: 16px;
            right: 16px;
            z-index: 2000;
            display: flex;
            flex-direction: column-reverse;
            gap: 8px;
            max-width: 380px;
        `;
        document.body.appendChild(container);
    }

    const colorMap = {
        success: '#057642',
        error: '#CC1016',
        info: '#0A66C2',
    };

    const toast = document.createElement('div');
    toast.style.cssText = `
        background: ${colorMap[type] || colorMap.success};
        color: #FFFFFF;
        font-size: 14px;
        padding: 10px 16px;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        animation: slideInRight 300ms ease-out;
        cursor: pointer;
        max-width: 380px;
        word-wrap: break-word;
    `;
    toast.textContent = message;
    toast.addEventListener('click', () => toast.remove());

    container.appendChild(toast);

    // Auto-remove
    setTimeout(() => {
        toast.style.animation = 'fadeOut 200ms ease-out forwards';
        setTimeout(() => toast.remove(), 200);
    }, duration);
}

// Add toast animations
const toastStyles = document.createElement('style');
toastStyles.textContent = `
    @keyframes slideInRight {
        from { opacity: 0; transform: translateX(100%); }
        to   { opacity: 1; transform: translateX(0); }
    }
    @keyframes fadeOut {
        to { opacity: 0; transform: translateY(-10px); }
    }
`;
document.head.appendChild(toastStyles);


/* ── Time Formatting ───────────────────────── */

/**
 * Formats a date string into a human-readable relative time.
 * - < 60 seconds: "Just now"
 * - < 60 minutes: "Xm ago"
 * - < 24 hours: "Xh ago"
 * - < 7 days: "Xd ago"
 * - >= 7 days: "Jan 15" or "Jan 15, 2024" if different year
 *
 * @param {string} dateString - ISO date string
 * @returns {string}
 */
function formatTimeAgo(dateString) {
    if (!dateString) return '';

    const now = new Date();
    const date = new Date(dateString);
    const seconds = Math.floor((now - date) / 1000);

    if (seconds < 60) return 'Just now';
    if (seconds < 3600) return `${Math.floor(seconds / 60)}m ago`;
    if (seconds < 86400) return `${Math.floor(seconds / 3600)}h ago`;
    if (seconds < 604800) return `${Math.floor(seconds / 86400)}d ago`;

    // >= 7 days: show date
    const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                    'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
    const month = months[date.getMonth()];
    const day = date.getDate();

    if (date.getFullYear() !== now.getFullYear()) {
        return `${month} ${day}, ${date.getFullYear()}`;
    }
    return `${month} ${day}`;
}

/**
 * Legacy alias for backward compatibility.
 */
function timeAgo(dateString) {
    return formatTimeAgo(dateString);
}


/* ── Initials Avatar ──────────────────────── */
/**
 * Generates an inline SVG data URL of a colored circle with
 * the first 2 letters of the username.
 * @param {string} username
 * @param {number} size - pixel size of the SVG
 * @returns {string} data URL
 */
function getInitialsAvatar(username, size = 48) {
    const colors = ['#0A66C2', '#057642', '#B24020', '#8B3A8F', '#C37D16'];
    let charSum = 0;
    for (let i = 0; i < username.length; i++) {
        charSum += username.charCodeAt(i);
    }
    const color = colors[charSum % colors.length];
    const initials = username.substring(0, 2).toUpperCase();
    const fontSize = Math.round(size * 0.4);

    const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="${size}" height="${size}" viewBox="0 0 ${size} ${size}">
        <rect width="${size}" height="${size}" rx="${size / 2}" fill="${color}"/>
        <text x="50%" y="50%" dy=".1em" fill="white" font-family="-apple-system,BlinkMacSystemFont,Segoe UI,Roboto,sans-serif" font-size="${fontSize}" font-weight="600" text-anchor="middle" dominant-baseline="central">${initials}</text>
    </svg>`;

    return 'data:image/svg+xml,' + encodeURIComponent(svg);
}


/* ── HTML Escaping ─────────────────────────── */
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}


/* ── Image Lightbox ────────────────────────── */

/**
 * Opens a full-screen lightbox overlay with the given image URL.
 * Press Escape, click the × button, or click the overlay to close.
 *
 * @param {string} imageUrl - The URL of the image to display
 */
function openLightbox(imageUrl) {
    // Prevent duplicates
    const existing = document.getElementById('lightbox-overlay');
    if (existing) existing.remove();

    const overlay = document.createElement('div');
    overlay.id = 'lightbox-overlay';
    overlay.className = 'lightbox-overlay';

    overlay.innerHTML = `
        <button class="lightbox-close" aria-label="Close lightbox">&times;</button>
        <img class="lightbox-image" src="${imageUrl}" alt="Full size image">
    `;

    // Close on overlay click (but not on image click)
    overlay.addEventListener('click', (e) => {
        if (e.target === overlay) closeLightbox();
    });

    // Close button
    overlay.querySelector('.lightbox-close').addEventListener('click', closeLightbox);

    document.body.appendChild(overlay);
    document.body.style.overflow = 'hidden';

    // Escape key
    document.addEventListener('keydown', lightboxEscapeHandler);
}

function closeLightbox() {
    const overlay = document.getElementById('lightbox-overlay');
    if (overlay) {
        overlay.style.animation = 'fadeOut 150ms ease forwards';
        setTimeout(() => {
            overlay.remove();
            document.body.style.overflow = '';
        }, 150);
    }
    document.removeEventListener('keydown', lightboxEscapeHandler);
}

function lightboxEscapeHandler(e) {
    if (e.key === 'Escape') closeLightbox();
}


/* ── Notification System ───────────────────── */
const NOTIFICATION_KEY = 'conectio_notifications';
const NOTIFICATION_READ_KEY = 'conectio_notifications_read';
const MAX_NOTIFICATIONS = 20;

/**
 * Add a notification message to localStorage.
 * @param {string} message - e.g. "You liked John's post"
 * @param {string} icon - emoji icon (default: "🔔")
 */
function addNotification(message, icon = '🔔') {
    const notifications = getNotifications();
    notifications.unshift({
        message,
        icon,
        time: new Date().toISOString(),
    });

    // Keep only last N
    if (notifications.length > MAX_NOTIFICATIONS) {
        notifications.length = MAX_NOTIFICATIONS;
    }

    localStorage.setItem(NOTIFICATION_KEY, JSON.stringify(notifications));
    localStorage.setItem(NOTIFICATION_READ_KEY, 'false');

    // Update the bell dot
    updateNotificationDot();
    // Update dropdown contents if open
    renderNotificationList();
}

/**
 * Get all notifications from localStorage.
 * @returns {Array<{message: string, icon: string, time: string}>}
 */
function getNotifications() {
    try {
        return JSON.parse(localStorage.getItem(NOTIFICATION_KEY)) || [];
    } catch {
        return [];
    }
}

/**
 * Clear all notifications.
 */
function clearNotifications() {
    localStorage.setItem(NOTIFICATION_KEY, JSON.stringify([]));
    localStorage.setItem(NOTIFICATION_READ_KEY, 'true');
    updateNotificationDot();
    renderNotificationList();
}

/**
 * Get count of unread notifications.
 */
function getUnreadNotificationCount() {
    const isRead = localStorage.getItem(NOTIFICATION_READ_KEY);
    if (isRead === 'true') return 0;
    return getNotifications().length;
}

/**
 * Mark notifications as read.
 */
function markNotificationsRead() {
    localStorage.setItem(NOTIFICATION_READ_KEY, 'true');
    updateNotificationDot();
}

/**
 * Update the red dot visibility on the bell icon.
 */
function updateNotificationDot() {
    const dot = document.getElementById('notification-dot');
    const count = getUnreadNotificationCount();

    if (count > 0 && !dot) {
        // Add dot
        const bell = document.getElementById('notification-bell');
        if (bell) {
            const newDot = document.createElement('span');
            newDot.className = 'notification-dot';
            newDot.id = 'notification-dot';
            bell.appendChild(newDot);
        }
    } else if (count === 0 && dot) {
        dot.remove();
    }
}

/**
 * Render the notification list inside the dropdown.
 */
function renderNotificationList() {
    const list = document.getElementById('notification-list');
    if (!list) return;

    const notifications = getNotifications();

    if (notifications.length === 0) {
        list.innerHTML = '<div class="notification-dropdown__empty">No notifications yet</div>';
        return;
    }

    list.innerHTML = notifications.slice(0, 5).map(n => `
        <div class="notification-dropdown__item">
            <span class="notification-dropdown__item-icon">${n.icon}</span>
            <div>
                <div>${escapeHtml(n.message)}</div>
                <div class="notification-dropdown__item-time">${formatTimeAgo(n.time)}</div>
            </div>
        </div>
    `).join('');
}

/**
 * Setup notification bell click behavior.
 */
function setupNotificationBell() {
    // Use event delegation since bell is rendered dynamically
    document.addEventListener('click', (e) => {
        const bell = e.target.closest('#notification-bell');
        const dropdown = document.getElementById('notification-dropdown');

        if (bell && dropdown) {
            // Don't toggle if clicking clear button
            if (e.target.closest('#notification-clear-btn')) {
                clearNotifications();
                return;
            }

            const isOpen = dropdown.classList.contains('notification-dropdown--open');
            dropdown.classList.toggle('notification-dropdown--open');

            if (!isOpen) {
                // Opening — mark as read and render list
                markNotificationsRead();
                renderNotificationList();
            }
        } else if (dropdown && !e.target.closest('#notification-dropdown')) {
            // Clicking outside — close
            dropdown.classList.remove('notification-dropdown--open');
        }
    });
}


/* ── Password Strength ─────────────────────── */

/**
 * Calculate password strength: weak, medium, or strong.
 * @param {string} password
 * @returns {'weak'|'medium'|'strong'}
 */
function getPasswordStrength(password) {
    let score = 0;
    if (password.length >= 8) score++;
    if (password.length >= 12) score++;
    if (/[a-z]/.test(password) && /[A-Z]/.test(password)) score++;
    if (/\d/.test(password)) score++;
    if (/[^a-zA-Z0-9]/.test(password)) score++;

    if (score <= 2) return 'weak';
    if (score <= 3) return 'medium';
    return 'strong';
}


/* ── Form Validation Helpers ───────────────── */

/**
 * Validate a username: letters, numbers, underscores, 3-30 chars.
 * @param {string} value
 * @returns {string|null} error message or null if valid
 */
function validateUsername(value) {
    if (!value) return 'Username is required.';
    if (value.length < 3) return 'Username must be at least 3 characters.';
    if (value.length > 30) return 'Username must be 30 characters or fewer.';
    if (!/^[a-zA-Z0-9_]+$/.test(value)) return 'Only letters, numbers, and underscores allowed.';
    return null;
}

/**
 * Validate an email address.
 * @param {string} value
 * @returns {string|null} error message or null if valid
 */
function validateEmail(value) {
    if (!value) return 'Email is required.';
    // Must contain @ and valid TLD
    if (!/^[^\s@]+@[^\s@]+\.[a-zA-Z]{2,}$/.test(value)) return 'Please enter a valid email address.';
    return null;
}

/**
 * Validate a password.
 * @param {string} value
 * @returns {string|null} error message or null if valid
 */
function validatePassword(value) {
    if (!value) return 'Password is required.';
    if (value.length < 8) return 'Password must be at least 8 characters.';
    return null;
}

/**
 * Show or clear inline field validation.
 * @param {string} inputId - The input element ID
 * @param {string|null} error - Error message or null if valid
 */
function setFieldValidation(inputId, error) {
    const input = document.getElementById(inputId);
    const errorEl = document.getElementById(inputId + '-error');
    if (!input) return;

    if (error) {
        input.classList.add('input-field--error');
        input.classList.remove('input-field--success');
        if (errorEl) {
            errorEl.textContent = error;
            errorEl.style.display = 'block';
        }
    } else if (input.value.trim()) {
        input.classList.remove('input-field--error');
        input.classList.add('input-field--success');
        if (errorEl) {
            errorEl.style.display = 'none';
        }
    } else {
        input.classList.remove('input-field--error', 'input-field--success');
        if (errorEl) {
            errorEl.style.display = 'none';
        }
    }
}


/* ── Export utilities ──────────────────────── */
window.app = {
    renderNavbar,
    showToast,
    timeAgo,
    formatTimeAgo,
    getInitialsAvatar,
    escapeHtml,
    openLightbox,
    closeLightbox,
    addNotification,
    getNotifications,
    clearNotifications,
    getPasswordStrength,
    validateUsername,
    validateEmail,
    validatePassword,
    setFieldValidation,
};
