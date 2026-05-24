/* ═══════════════════════════════════════════════
   CONECTIO — Auth Module
   Token management and authentication helpers
   ═══════════════════════════════════════════════ */

const TOKEN_KEY = 'conectio_access_token';
const REFRESH_KEY = 'conectio_refresh_token';

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
 * Remove all auth tokens (logout).
 */
function removeToken() {
    localStorage.removeItem(TOKEN_KEY);
    localStorage.removeItem(REFRESH_KEY);
}

/**
 * Check if the user is logged in (token exists).
 * @returns {boolean}
 */
function isLoggedIn() {
    const token = getToken();
    if (!token) return false;

    // Check if token is expired
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
 * Get the current user info from the JWT.
 * @returns {object|null} - { user_id, username, email }
 */
function getCurrentUser() {
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
 * Logout the user and redirect to home.
 */
function logout() {
    removeToken();
    window.location.href = 'index.html';
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
            usernameEl.textContent = user.username || 'Me';
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
    removeToken,
    isLoggedIn,
    getCurrentUser,
    redirectIfNotLoggedIn,
    redirectIfLoggedIn,
    logout,
    updateNavbar,
    parseJWT,
};
