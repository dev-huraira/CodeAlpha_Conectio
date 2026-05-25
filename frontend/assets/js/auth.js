/* ═══════════════════════════════════════════════
   CONECTIO — Auth Module
   Token management and authentication helpers
   ═══════════════════════════════════════════════ */

const TOKEN_KEY = 'conectio_access';
const REFRESH_KEY = 'conectio_refresh';
const USER_KEY = 'conectio_user';


/* ── Token Management ──────────────────────── */

/**
 * Save JWT tokens to localStorage.
 * @param {string} access  - Access token
 * @param {string} refresh - Refresh token
 */
function saveToken(access, refresh) {
    localStorage.setItem(TOKEN_KEY, access);
    if (refresh) {
        localStorage.setItem(REFRESH_KEY, refresh);
    }
}

/**
 * Get the current access token.
 * @returns {string|null}
 */
function getToken() {
    return localStorage.getItem(TOKEN_KEY);
}

/**
 * Get the current refresh token.
 * @returns {string|null}
 */
function getRefreshToken() {
    return localStorage.getItem(REFRESH_KEY);
}

/**
 * Save the user object to localStorage.
 * @param {object} userObj - User data from the API
 */
function saveUser(userObj) {
    localStorage.setItem(USER_KEY, JSON.stringify(userObj));
}

/**
 * Get the cached user object.
 * @returns {object|null}
 */
function getUser() {
    try {
        return JSON.parse(localStorage.getItem(USER_KEY));
    } catch {
        return null;
    }
}

/**
 * Remove all auth data from localStorage (logout).
 */
function removeToken() {
    localStorage.removeItem(TOKEN_KEY);
    localStorage.removeItem(REFRESH_KEY);
    localStorage.removeItem(USER_KEY);
}

/**
 * Check if the user is logged in (token exists and not expired).
 * @returns {boolean}
 */
function isLoggedIn() {
    const token = getToken();
    if (!token) return false;

    try {
        const payload = parseJWT(token);
        const now = Math.floor(Date.now() / 1000);
        return payload.exp > now;
    } catch {
        return false;
    }
}

/**
 * Decode JWT payload without verification.
 * @param {string} token
 * @returns {object} - Decoded payload
 */
function parseJWT(token) {
    const base64Url = token.split('.')[1];
    const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
    const jsonPayload = decodeURIComponent(
        atob(base64)
            .split('')
            .map(c => '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2))
            .join('')
    );
    return JSON.parse(jsonPayload);
}

/**
 * Get the current user info — prefers cached user object, falls back to JWT.
 * @returns {object|null}
 */
function getCurrentUser() {
    // First try the cached full user object
    const cached = getUser();
    if (cached) return cached;

    // Fallback: extract from JWT
    const token = getToken();
    if (!token) return null;

    try {
        const payload = parseJWT(token);
        return {
            id: payload.user_id,
            username: payload.username || null,
            email: payload.email || null,
        };
    } catch {
        return null;
    }
}

/**
 * Redirect to login page if user is not logged in.
 */
function redirectIfNotLoggedIn() {
    if (!isLoggedIn()) {
        window.location.href = 'login.html';
    }
}

/**
 * Redirect to home page if user is already logged in.
 */
function redirectIfLoggedIn() {
    if (isLoggedIn()) {
        window.location.href = 'index.html';
    }
}

/**
 * Logout the user — blacklist token server-side, clear storage, redirect.
 */
async function logout() {
    const refreshToken = getRefreshToken();
    const accessToken = getToken();

    // Try to blacklist the refresh token on the server
    if (refreshToken && accessToken) {
        try {
            await fetch(`${window.api.BASE}/users/logout/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${accessToken}`,
                },
                body: JSON.stringify({ refresh: refreshToken }),
            });
        } catch {
            // Ignore errors — we'll clear local storage regardless
        }
    }

    removeToken();
    window.location.href = 'login.html';
}

/**
 * Update the navbar based on auth state.
 */
function updateNavbar() {
    const authNav = document.getElementById('nav-auth');
    const userNav = document.getElementById('nav-user');

    if (!authNav || !userNav) return;

    if (isLoggedIn()) {
        authNav.style.display = 'none';
        userNav.style.display = 'flex';

        const user = getCurrentUser();
        const usernameEl = document.getElementById('nav-username');
        if (usernameEl && user) {
            usernameEl.textContent = user.first_name || user.username || 'Me';
        }
    } else {
        authNav.style.display = 'flex';
        userNav.style.display = 'none';
    }
}


/* ── Export for use in other scripts ────────── */
window.auth = {
    saveToken,
    getToken,
    getRefreshToken,
    saveUser,
    getUser,
    removeToken,
    isLoggedIn,
    getCurrentUser,
    redirectIfNotLoggedIn,
    redirectIfLoggedIn,
    logout,
    updateNavbar,
    parseJWT,
};
