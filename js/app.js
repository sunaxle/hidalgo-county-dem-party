document.addEventListener('DOMContentLoaded', () => {
  const menuBtn = document.querySelector('.mobile-menu-btn');
  const navLinks = document.querySelector('.nav-links');

  if (menuBtn) {
    menuBtn.addEventListener('click', () => {
      navLinks.classList.toggle('active');
    });
  }

  // Mobile Dropdown Toggle (Accordion)
  const dropdowns = document.querySelectorAll('.dropdown');
  dropdowns.forEach(dropdown => {
    const span = dropdown.querySelector('span');
    if (span) {
      span.addEventListener('click', (e) => {
        if (window.innerWidth <= 768) {
          e.preventDefault();
          dropdown.classList.toggle('active');
        }
      });
    }
  });

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

  // --- Floating Webmaster Button ---
  const wmContainer = document.createElement('div');
  wmContainer.style.position = 'fixed';
  wmContainer.style.bottom = '20px';
  wmContainer.style.right = '20px';
  wmContainer.style.zIndex = '9999';
  wmContainer.style.display = 'flex';
  wmContainer.style.flexDirection = 'column';
  wmContainer.style.alignItems = 'flex-end';
  wmContainer.style.fontFamily = "'Inter', sans-serif";

  // Tooltip
  const wmTooltip = document.createElement('div');
  wmTooltip.style.background = 'rgba(15, 23, 42, 0.95)';
  wmTooltip.style.color = '#cbd5e1';
  wmTooltip.style.padding = '1.2rem';
  wmTooltip.style.borderRadius = '12px';
  wmTooltip.style.border = '1px solid #38bdf8';
  wmTooltip.style.boxShadow = '0 10px 30px rgba(0,0,0,0.6)';
  wmTooltip.style.marginBottom = '10px';
  wmTooltip.style.width = '280px';
  wmTooltip.style.fontSize = '0.9rem';
  wmTooltip.style.lineHeight = '1.5';
  wmTooltip.style.opacity = '0';
  wmTooltip.style.visibility = 'hidden';
  wmTooltip.style.transform = 'translateY(10px)';
  wmTooltip.style.transition = 'opacity 0.3s ease, transform 0.3s ease, visibility 0.3s';
  wmTooltip.innerHTML = `
    <strong style="color: #fff; font-size: 1.1rem; display:block; margin-bottom:0.5rem;">Site Suggestions?</strong>
    If you have any suggestions, insights, or specific web updates for this platform, please send a WhatsApp voice memo or text to:
    <br/><br/>
    <a href="https://wa.me/19566387581" target="_blank" style="display:inline-block; background:#25D366; color:#fff; text-decoration:none; padding:0.6rem 1rem; border-radius:6px; font-weight:800; width:100%; text-align:center; box-sizing:border-box;">Message Webmaster</a>
    <div style="margin-top:0.8rem; text-align:center; font-size:0.85rem; color:#94a3b8;">📱 (956) 638-7581</div>
  `;

  // Button
  const wmBtn = document.createElement('div');
  wmBtn.style.background = 'var(--accent, #38bdf8)';
  wmBtn.style.color = '#020617';
  wmBtn.style.padding = '12px 24px';
  wmBtn.style.borderRadius = '30px';
  wmBtn.style.fontWeight = '800';
  wmBtn.style.cursor = 'pointer';
  wmBtn.style.boxShadow = '0 4px 15px rgba(0,0,0,0.3)';
  wmBtn.style.display = 'flex';
  wmBtn.style.alignItems = 'center';
  wmBtn.style.gap = '8px';
  wmBtn.style.transition = 'transform 0.2s, box-shadow 0.2s';
  wmBtn.style.border = '2px solid rgba(255,255,255,0.2)';
  wmBtn.innerHTML = `🛠️ Webmaster`;

  wmBtn.addEventListener('mouseenter', () => {
      wmBtn.style.transform = 'scale(1.05)';
      wmBtn.style.boxShadow = '0 4px 20px rgba(56, 189, 248, 0.6)';
      wmTooltip.style.opacity = '1';
      wmTooltip.style.visibility = 'visible';
      wmTooltip.style.transform = 'translateY(0)';
  });

  wmContainer.addEventListener('mouseleave', () => {
      wmBtn.style.transform = 'scale(1)';
      wmBtn.style.boxShadow = '0 4px 15px rgba(0,0,0,0.3)';
      wmTooltip.style.opacity = '0';
      wmTooltip.style.visibility = 'hidden';
      wmTooltip.style.transform = 'translateY(10px)';
  });

  wmContainer.appendChild(wmTooltip);
  wmContainer.appendChild(wmBtn);
  document.body.appendChild(wmContainer);

});
