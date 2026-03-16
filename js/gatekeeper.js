// js/gatekeeper.js
// Master Maintenance Gate for Hidalgo County Democratic Party
(function() {
    // Determine the current path
    const path = window.location.pathname;
    
    // Check if the user is currently on the root index page (The Maintenance Gate)
    const isMaintenancePage = path.endsWith('/index.html') || path === '/' || path.endsWith('/hidalgo-county-dem-party/') || path.endsWith('hidalgo-county-dem-party/index.html');
    
    // If we are NOT on the maintenance page, we must verify the session token
    if (!isMaintenancePage) {
        const hasAccess = sessionStorage.getItem('hcdp_maintenance_access');
        
        // If the token is missing or incorrect, aggressively redirect them back to the gate
        if (hasAccess !== 'granted_PC26') {
            console.warn("Access Denied: Rerouting to Maintenance Security Gate.");
            // We use a relative path to handle both local file:// testing and production subdirectories
            let depth = (path.match(/\//g) || []).length;
            // Simplified routing for flat directory structures
            window.location.href = 'index.html';
        }
    }
})();
