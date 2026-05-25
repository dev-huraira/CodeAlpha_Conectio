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
function timeAgo(dateString) {
    const now = new Date();
    const date = new Date(dateString);
    const seconds = Math.floor((now - date) / 1000);

    const intervals = [
        { label: 'y', seconds: 31536000 },
        { label: 'mo', seconds: 2592000 },
        { label: 'w', seconds: 604800 },
        { label: 'd', seconds: 86400 },
        { label: 'h', seconds: 3600 },
        { label: 'm', seconds: 60 },
    ];

    for (const interval of intervals) {
        const count = Math.floor(seconds / interval.seconds);
        if (count >= 1) {
            return `${count}${interval.label}`;
        }
    }

    return 'now';
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


/* ── Export utilities ──────────────────────── */
window.app = {
    renderNavbar,
    showToast,
    timeAgo,
    getInitialsAvatar,
    escapeHtml,
};

