// theme_switcher.js
// Injects a floating panel to test different CSS color schemes instantly

document.addEventListener('DOMContentLoaded', () => {
    // Create the floating panel
    const panel = document.createElement('div');
    panel.style.position = 'fixed';
    panel.style.bottom = '20px';
    panel.style.left = '20px';
    panel.style.zIndex = '9999';
    panel.style.background = 'rgba(15, 23, 42, 0.9)';
    panel.style.backdropFilter = 'blur(10px)';
    panel.style.border = '1px solid rgba(255, 255, 255, 0.2)';
    panel.style.padding = '15px';
    panel.style.borderRadius = '12px';
    panel.style.boxShadow = '0 10px 25px rgba(0,0,0,0.5)';
    panel.style.display = 'flex';
    panel.style.flexDirection = 'column';
    panel.style.gap = '10px';
    panel.style.color = 'white';
    panel.style.fontFamily = "'Inter', sans-serif";

    const title = document.createElement('div');
    title.innerText = '🎨 Live Theme Tester';
    title.style.fontWeight = 'bold';
    title.style.fontSize = '0.9rem';
    title.style.marginBottom = '5px';
    title.style.textAlign = 'center';
    panel.appendChild(title);

    const themes = [
        {
            name: 'Cyber-Navy (Original)',
            colors: {
                '--bg-dark': '#0f172a',
                '--glass-bg': 'rgba(30, 41, 59, 0.7)',
                '--accent': '#22d3ee',
                '--accent-hover': '#06b6d4',
                '--text-main': '#f8fafc',
                '--text-muted': '#94a3b8'
            }
        },
        {
            name: 'Texas Flag (Red/Blue)',
            colors: {
                '--bg-dark': '#0b132b',
                '--glass-bg': 'rgba(28, 37, 65, 0.8)',
                '--accent': '#e11d48', // Vibrant red
                '--accent-hover': '#be123c',
                '--text-main': '#ffffff',
                '--text-muted': '#cbd5e1'
            }
        },
        {
            name: 'Midnight Purple',
            colors: {
                '--bg-dark': '#2e1065', // Deep purple
                '--glass-bg': 'rgba(76, 29, 149, 0.5)',
                '--accent': '#d946ef', // Neon pink/purple
                '--accent-hover': '#c026d3',
                '--text-main': '#fdf4ff',
                '--text-muted': '#e879f9'
            }
        },
        {
            name: 'Eco-Green (Earthy)',
            colors: {
                '--bg-dark': '#064e3b', // Deep emerald
                '--glass-bg': 'rgba(6, 95, 70, 0.6)',
                '--accent': '#10b981', // Lime green
                '--accent-hover': '#059669',
                '--text-main': '#ecfdf5',
                '--text-muted': '#6ee7b7'
            }
        },
        {
            name: 'Sunset Orange',
            colors: {
                '--bg-dark': '#431407', // Deep orange-brown
                '--glass-bg': 'rgba(124, 45, 18, 0.6)',
                '--accent': '#f97316', // Vibrant orange
                '--accent-hover': '#ea580c',
                '--text-main': '#fff7ed',
                '--text-muted': '#fdba74'
            }
        }
    ];

    themes.forEach(theme => {
        const btn = document.createElement('button');
        btn.innerText = theme.name;
        btn.style.padding = '8px 12px';
        btn.style.border = 'none';
        btn.style.borderRadius = '6px';
        // Use the theme's background to preview the main dark color, and accent for border
        btn.style.background = theme.colors['--bg-dark'];
        btn.style.borderLeft = `4px solid ${theme.colors['--accent']}`;
        btn.style.color = 'white';
        btn.style.cursor = 'pointer';
        btn.style.fontWeight = 'bold';
        btn.style.fontSize = '0.8rem';
        btn.style.transition = 'opacity 0.2s';
        btn.style.textAlign = 'left';
        
        btn.onmouseover = () => btn.style.opacity = '0.8';
        btn.onmouseout = () => btn.style.opacity = '1';

        btn.onclick = () => {
            const root = document.documentElement;
            // Loop through custom colors and update CSS Variables on the :root element
            for (const [property, value] of Object.entries(theme.colors)) {
                root.style.setProperty(property, value);
            }
            // Ensure body text updates if we transition modes
            document.body.style.color = theme.colors['--text-main'];
        };

        panel.appendChild(btn);
    });

    // Append to body
    document.body.appendChild(panel);
});
