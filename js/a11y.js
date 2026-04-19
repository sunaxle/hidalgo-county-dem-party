document.addEventListener("DOMContentLoaded", () => {
    // 1. Inject the floating UI securely into the DOM
    const a11yHTML = `
        <div id="a11y-widget-container">
            <button id="a11y-toggle-btn" aria-label="Open Accessibility Menu" title="Accessibility Options">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <circle cx="12" cy="12" r="10"></circle>
                    <path d="M12 16v-4"></path>
                    <path d="M12 8h.01"></path>
                    <path d="M8 12h8"></path>
                </svg>
            </button>
            <div id="a11y-menu">
                <div class="a11y-menu-header">
                    Accessibility
                    <button class="a11y-close-btn" id="a11y-close-btn" aria-label="Close">&times;</button>
                </div>
                <div class="a11y-option">
                    <span>High Contrast</span>
                    <label class="a11y-switch" aria-label="Toggle High Contrast">
                        <input type="checkbox" id="a11y-hc-toggle">
                        <span class="a11y-slider"></span>
                    </label>
                </div>
                <div class="a11y-option">
                    <span>Large Text</span>
                    <label class="a11y-switch" aria-label="Toggle Large Text">
                        <input type="checkbox" id="a11y-lt-toggle">
                        <span class="a11y-slider"></span>
                    </label>
                </div>
                <div class="a11y-option">
                    <span>Reduce Motion</span>
                    <label class="a11y-switch" aria-label="Toggle Reduce Motion">
                        <input type="checkbox" id="a11y-rm-toggle">
                        <span class="a11y-slider"></span>
                    </label>
                </div>
            </div>
        </div>
    `;

    document.body.insertAdjacentHTML('beforeend', a11yHTML);

    // 2. Cache DOM elements
    const toggleBtn = document.getElementById('a11y-toggle-btn');
    const closeBtn = document.getElementById('a11y-close-btn');
    const menu = document.getElementById('a11y-menu');
    const hcToggle = document.getElementById('a11y-hc-toggle');
    const ltToggle = document.getElementById('a11y-lt-toggle');
    const rmToggle = document.getElementById('a11y-rm-toggle');

    // 3. UI Interactions
    toggleBtn.addEventListener('click', () => menu.classList.toggle('active'));
    closeBtn.addEventListener('click', () => menu.classList.remove('active'));

    // 4. Preference Synchronization
    const applyPreferences = () => {
        // High Contrast
        if (hcToggle.checked) {
            document.body.classList.add('a11y-high-contrast');
            localStorage.setItem('a11y-hc', 'true');
        } else {
            document.body.classList.remove('a11y-high-contrast');
            localStorage.setItem('a11y-hc', 'false');
        }

        // Large Text
        if (ltToggle.checked) {
            document.body.classList.add('a11y-large-text');
            localStorage.setItem('a11y-lt', 'true');
        } else {
            document.body.classList.remove('a11y-large-text');
            localStorage.setItem('a11y-lt', 'false');
        }

        // Reduced Motion
        if (rmToggle.checked) {
            document.body.classList.add('a11y-reduced-motion');
            localStorage.setItem('a11y-rm', 'true');
        } else {
            document.body.classList.remove('a11y-reduced-motion');
            localStorage.setItem('a11y-rm', 'false');
        }
    };

    // 5. Event Listeners for Toggles
    hcToggle.addEventListener('change', applyPreferences);
    ltToggle.addEventListener('change', applyPreferences);
    rmToggle.addEventListener('change', applyPreferences);

    // 6. Initial Load Check
    if (localStorage.getItem('a11y-hc') === 'true') hcToggle.checked = true;
    if (localStorage.getItem('a11y-lt') === 'true') ltToggle.checked = true;
    if (localStorage.getItem('a11y-rm') === 'true') rmToggle.checked = true;
    
    // Apply state to body instantly
    applyPreferences();
});
