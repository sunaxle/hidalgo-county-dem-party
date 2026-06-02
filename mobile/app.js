document.addEventListener("DOMContentLoaded", () => {
    // Add a simple fade-in effect to simulate native page transitions
    document.body.style.opacity = '0';
    document.body.style.transition = 'opacity 0.2s ease-in-out';
    
    setTimeout(() => {
        document.body.style.opacity = '1';
    }, 10);

    // Remove legacy hamburger logic
    // Bottom tab active states are managed via hardcoded HTML classes in the prototype
});
