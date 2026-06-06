/* ═══════════════════════════════════════════════
   CONECTIO — API Client
   Centralized fetch wrapper with JWT auth
   ═══════════════════════════════════════════════ */

const API_BASE = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
    ? 'http://localhost:8000/api'
    : 'https://YOUR-RENDER-URL.onrender.com/api';

/**
 * Core fetch wrapper that automatically attaches JWT tokens,
 * handles JSON parsing, and throws on error responses.
 *
 * @param {string} endpoint - API path (e.g., '/users/profile/')
 * @param {object} options  - fetch options (method, body, headers, etc.)
 * @returns {Promise<any>}  - Parsed JSON response
 */
async function apiFetch(endpoint, options = {}) {
    const url = `${API_BASE}${endpoint}`;
    const token = localStorage.getItem('conectio_access');

    const headers = {
        ...(options.headers || {}),
    };

    // Only set Content-Type to JSON if body is not FormData
    if (!(options.body instanceof FormData)) {
        headers['Content-Type'] = 'application/json';
    }

    // Attach JWT token if available
    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }

    const config = {
        ...options,
        headers,
    };

    // Stringify body if it's a plain object
    if (config.body && typeof config.body === 'object' && !(config.body instanceof FormData)) {
        config.body = JSON.stringify(config.body);
    }

    try {
        const response = await fetch(url, config);

        // Handle 204 No Content
        if (response.status === 204) {
            return null;
        }

        const data = await response.json().catch(() => null);

        if (!response.ok) {
            const error = new Error(data?.detail || data?.message || `Request failed (${response.status})`);
            error.status = response.status;
            error.data = data;
            throw error;
        }

        return data;
    } catch (err) {
        // Re-throw API errors, wrap network errors
        if (err.status) throw err;
        const networkError = new Error('Network error. Please check your connection.');
        networkError.status = 0;
        throw networkError;
    }
}


/**
 * GET request
 * @param {string} endpoint
 * @returns {Promise<any>}
 */
async function apiGet(endpoint) {
    return apiFetch(endpoint, { method: 'GET' });
}

/**
 * POST request
 * @param {string} endpoint
 * @param {object|FormData} body
 * @returns {Promise<any>}
 */
async function apiPost(endpoint, body = {}) {
    return apiFetch(endpoint, { method: 'POST', body });
}

/**
 * PATCH request
 * @param {string} endpoint
 * @param {object|FormData} body
 * @returns {Promise<any>}
 */
async function apiPatch(endpoint, body = {}) {
    return apiFetch(endpoint, { method: 'PATCH', body });
}

/**
 * DELETE request
 * @param {string} endpoint
 * @returns {Promise<any>}
 */
async function apiDelete(endpoint) {
    return apiFetch(endpoint, { method: 'DELETE' });
}


/* ── Export for use in other scripts ────────── */
// Using window globals since we're not using a bundler
window.api = {
    fetch: apiFetch,
    get: apiGet,
    post: apiPost,
    patch: apiPatch,
    delete: apiDelete,
    BASE: API_BASE,
};
