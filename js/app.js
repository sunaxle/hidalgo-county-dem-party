document.addEventListener('DOMContentLoaded', () => {
  // Mobile Menu Toggle
  const menuBtn = document.querySelector('.mobile-menu-btn');
  const navLinks = document.querySelector('.nav-links');

  if (menuBtn) {
    menuBtn.addEventListener('click', () => {
      navLinks.classList.toggle('active');
    });
  }

  // Navbar Scroll Effect
  const navbar = document.querySelector('.navbar');
  window.addEventListener('scroll', () => {
    if (window.scrollY > 50) {
      navbar.classList.add('scrolled');
    } else {
      navbar.classList.remove('scrolled');
    }
  });

  // Fade In Animations using Intersection Observer
  const observerOptions = {
    threshold: 0.1,
    rootMargin: "0px 0px -50px 0px"
  };

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        observer.unobserve(entry.target);
      }
    });
  }, observerOptions);

  const fadeElements = document.querySelectorAll('.fade-in');
  fadeElements.forEach(el => observer.observe(el));

  // --- Spanish Theme Override (Mexican Flag Colors) ---
  const applyMexicanTheme = () => {
    const root = document.documentElement;
    root.style.setProperty('--bg-dark', '#064e3b');      // Deep emerald green background
    root.style.setProperty('--glass-bg', 'rgba(6, 95, 70, 0.7)'); // Lighter green glass
    root.style.setProperty('--primary', '#ef4444');      // Vibrant red
    root.style.setProperty('--primary-hover', '#dc2626');
    root.style.setProperty('--accent', '#ef4444');       // Vibrant red for accents
    root.style.setProperty('--accent-hover', '#b91c1c');
    root.style.setProperty('--bg-gradient', 'linear-gradient(135deg, #064e3b 0%, #022c22 100%)');
    
    // Ensure White Text is enforced across specific dynamically colored components
    document.body.style.color = '#ffffff';
    root.style.setProperty('--text-main', '#ffffff');
    root.style.setProperty('--text-muted', '#fbbf24'); // Yellow/Gold text for accents
  };

  const removeMexicanTheme = () => {
    const root = document.documentElement;
    root.style.removeProperty('--bg-dark');
    root.style.removeProperty('--glass-bg');
    root.style.removeProperty('--primary');
    root.style.removeProperty('--primary-hover');
    root.style.removeProperty('--accent');
    root.style.removeProperty('--accent-hover');
    root.style.removeProperty('--bg-gradient');
    
    document.body.style.color = '';
    root.style.removeProperty('--text-main');
    root.style.removeProperty('--text-muted');
  };

  const checkLanguageState = () => {
    // Google Translate sets a cookie: googtrans=/auto/es or /en/es
    const isSpanish = document.cookie.includes('googtrans=/en/es') || document.cookie.includes('googtrans=/auto/es');
    
    // Also check the HTML class for safety as it adds 'translated-ltr'
    const htmlEl = document.documentElement;
    const hasClass = htmlEl.classList.contains('translated-ltr') || htmlEl.classList.contains('translated-rtl');
    
    if (isSpanish || hasClass) {
        applyMexicanTheme();
    } else {
        removeMexicanTheme();
    }
  };

  // Google injects scripts that modify the DOM after load. We use a MutationObserver to watch the <html> tag.
  const langObserver = new MutationObserver((mutations) => {
    mutations.forEach((mutation) => {
        if (mutation.attributeName === 'class' || mutation.attributeName === 'lang') {
            checkLanguageState();
        }
    });
  });

  // Start observing the <html> tag for changes made by the translation widget
  langObserver.observe(document.documentElement, { attributes: true });

  // Safety check on initial load (in case they reload the page and the cookie is already set)
  setTimeout(checkLanguageState, 1500);

});
