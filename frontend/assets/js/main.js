/* ═══════════════════════════════════════════════
   CONECTIO — Main Application Logic
   Page-specific initialization and shared utilities
   ═══════════════════════════════════════════════ */

document.addEventListener('DOMContentLoaded', () => {
    // Update navbar auth state on every page
    if (window.auth) {
        window.auth.updateNavbar();
    }

    // Setup mobile menu toggle
    setupMobileMenu();

    // Setup dropdown menus
    setupDropdowns();
});


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
    showToast,
    timeAgo,
};
