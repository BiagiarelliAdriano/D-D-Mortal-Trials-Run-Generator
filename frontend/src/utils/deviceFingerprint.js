/**
 * Device fingerprinting utility.
 * Generates a lightweight, deterministic fingerprint from publicly available
 * browser properties. Not cryptographically strong, but sufficient to reliably
 * distinguish "my usual browser" from "a new/different device".
 *
 * No sensitive user data is ever included in the fingerprint.
 */

/**
 * Produces a short hash string representing the current browser environment.
 * @returns {string} A base-36 hash of browser properties.
 */
export function getDeviceFingerprint() {
    const components = [
        navigator.userAgent,
        navigator.language,
        `${window.screen.width}x${window.screen.height}`,
        Intl.DateTimeFormat().resolvedOptions().timeZone,
        String(navigator.hardwareConcurrency ?? 'unknown'),
        navigator.platform ?? 'unknown',
    ].join('|||');

    // djb2 hash — fast, consistent, no external deps
    let hash = 5381;
    for (let i = 0; i < components.length; i++) {
        hash = ((hash << 5) + hash) ^ components.charCodeAt(i);
        hash = hash >>> 0; // keep unsigned 32-bit integer
    }
    return hash.toString(36);
}

/**
 * Determines whether the current login attempt should trigger a security
 * question challenge. Returns true when:
 *   - No trusted device fingerprint is stored (new device / cleared browser data)
 *   - The stored fingerprint doesn't match this browser (different device)
 *   - The `needs_reauth` flag was set because the JWT expired naturally
 *
 * Explicit logout does NOT set `needs_reauth`, so same-device re-login
 * after a manual logout will NOT trigger the challenge.
 *
 * @returns {boolean}
 */
export function needsSecurityChallenge() {
    const storedFingerprint = localStorage.getItem('device_fingerprint');
    const currentFingerprint = getDeviceFingerprint();
    const tokenExpiredFlag = localStorage.getItem('needs_reauth') === 'true';

    // New or different device
    if (!storedFingerprint || storedFingerprint !== currentFingerprint) {
        return true;
    }

    // Token expired naturally on this same device
    if (tokenExpiredFlag) {
        return true;
    }

    return false;
}
