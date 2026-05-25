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
function showToast(message, type = 'info', duration = 4000) {
    // Create toast container if it doesn't exist
    let container = document.getElementById('toast-container');
    if (!container) {
        container = document.createElement('div');
        container.id = 'toast-container';
        container.style.cssText = `
            position: fixed;
            top: 68px;
            right: 16px;
            z-index: 2000;
            display: flex;
            flex-direction: column;
            gap: 8px;
            max-width: 380px;
        `;
        document.body.appendChild(container);
    }

    const toast = document.createElement('div');
    toast.className = `alert alert--${type}`;
    toast.style.cssText = `
        animation: slideInRight 300ms ease-out;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    `;
    toast.textContent = message;

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


/* ── Export utilities ──────────────────────── */
window.app = {
    renderNavbar,
    showToast,
    timeAgo,
};
