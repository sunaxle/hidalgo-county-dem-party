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
      // Force hardware constraints dynamically for iOS Safari caches
      span.style.webkitUserSelect = 'none';
      span.style.userSelect = 'none';
      span.style.webkitTouchCallout = 'none';
      span.style.cursor = 'pointer';
      span.style.webkitTapHighlightColor = 'transparent';

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

  // Button - Subtle & Faded State
  const wmBtn = document.createElement('div');
  wmBtn.style.background = 'rgba(15, 23, 42, 0.5)';
  wmBtn.style.color = 'rgba(203, 213, 225, 0.6)'; // Muted text
  wmBtn.style.padding = '8px 16px'; // smaller internal padding
  wmBtn.style.fontSize = '0.85rem'; // smaller font size
  wmBtn.style.borderRadius = '30px';
  wmBtn.style.fontWeight = '600';
  wmBtn.style.cursor = 'pointer';
  wmBtn.style.boxShadow = '0 2px 10px rgba(0,0,0,0.2)';
  wmBtn.style.display = 'flex';
  wmBtn.style.alignItems = 'center';
  wmBtn.style.gap = '6px';
  wmBtn.style.opacity = '0.6'; // extremely faded initially
  wmBtn.style.backdropFilter = 'blur(4px)';
  wmBtn.style.transition = 'all 0.3s ease';
  wmBtn.style.border = '1px solid rgba(255,255,255,0.1)';
  wmBtn.innerHTML = `🛠️ Webmaster`;

  const activateWM = () => {
      wmBtn.style.background = 'var(--accent, #38bdf8)';
      wmBtn.style.color = '#020617';
      wmBtn.style.opacity = '1';
      wmBtn.style.border = '1px solid rgba(255,255,255,0.4)';
      wmBtn.style.transform = 'scale(1.1)';
      wmBtn.style.boxShadow = '0 4px 20px rgba(56, 189, 248, 0.6)';
      wmTooltip.style.opacity = '1';
      wmTooltip.style.visibility = 'visible';
      wmTooltip.style.transform = 'translateY(0)';
  };

  const deactivateWM = () => {
      wmBtn.style.background = 'rgba(15, 23, 42, 0.5)';
      wmBtn.style.color = 'rgba(203, 213, 225, 0.6)';
      wmBtn.style.opacity = '0.6';
      wmBtn.style.border = '1px solid rgba(255,255,255,0.1)';
      wmBtn.style.transform = 'scale(1)';
      wmBtn.style.boxShadow = '0 2px 10px rgba(0,0,0,0.2)';
      wmTooltip.style.opacity = '0';
      wmTooltip.style.visibility = 'hidden';
      wmTooltip.style.transform = 'translateY(10px)';
  };

  // Desktop Hover Paths
  wmBtn.addEventListener('mouseenter', () => { if (window.innerWidth > 768) activateWM(); });
  wmContainer.addEventListener('mouseleave', () => { if (window.innerWidth > 768) deactivateWM(); });

  // Mobile Tap-to-Toggle Path
  wmBtn.addEventListener('click', (e) => {
      if (window.innerWidth <= 768) {
          e.stopPropagation();
          (wmBtn.style.opacity === '1') ? deactivateWM() : activateWM();
      }
  });

  // Tap outside to close on mobile
  document.addEventListener('click', (e) => {
      if (window.innerWidth <= 768 && !wmContainer.contains(e.target)) {
          deactivateWM();
      }
  });

  wmContainer.appendChild(wmTooltip);
  wmContainer.appendChild(wmBtn);
  document.body.appendChild(wmContainer);

  // --- Mobile Experience Warning Popup ---
  if (window.innerWidth <= 768 && !sessionStorage.getItem('mobile_warning_seen')) {
    const warningOverlay = document.createElement('div');
    warningOverlay.style.position = 'fixed';
    warningOverlay.style.top = '0';
    warningOverlay.style.left = '0';
    warningOverlay.style.width = '100vw';
    warningOverlay.style.height = '100vh';
    warningOverlay.style.backgroundColor = 'rgba(2, 6, 23, 0.85)';
    warningOverlay.style.backdropFilter = 'blur(8px)';
    warningOverlay.style.webkitBackdropFilter = 'blur(8px)';
    warningOverlay.style.zIndex = '10000';
    warningOverlay.style.display = 'flex';
    warningOverlay.style.justifyContent = 'center';
    warningOverlay.style.alignItems = 'center';
    warningOverlay.style.padding = '2rem';
    warningOverlay.style.boxSizing = 'border-box';

    const warningBox = document.createElement('div');
    warningBox.style.background = 'linear-gradient(145deg, #1e293b, #0f172a)';
    warningBox.style.border = '1px solid #38bdf8';
    warningBox.style.borderRadius = '16px';
    warningBox.style.padding = '2.5rem 2rem';
    warningBox.style.textAlign = 'center';
    warningBox.style.boxShadow = '0 25px 50px -12px rgba(0,0,0,0.7)';
    warningBox.style.maxWidth = '400px';

    warningBox.innerHTML = `
      <div style="font-size: 3.5rem; margin-bottom: 1rem;">⚠️</div>
      <h3 style="color: #38bdf8; font-size: 1.5rem; margin-bottom: 1rem; margin-top:0;">Mobile Optimization In Progress</h3>
      <p style="color: #cbd5e1; font-size: 1.05rem; line-height: 1.6; margin-bottom: 2rem;">
        Welcome to the new platform! This is the first week of deployment and many user experience updates are still being finalized for mobile devices.
        <br><br>
        For the best possible experience today, please open this site on an <strong>iPad or Desktop Computer</strong>.
      </p>
      <button id="closeMobileWarning" style="background: #38bdf8; color: #020617; border: none; padding: 1rem 2rem; border-radius: 8px; font-weight: 800; font-size: 1.1rem; cursor: pointer; width: 100%; transition: background 0.3s; text-transform: uppercase;">Continue Anyway</button>
    `;

    warningOverlay.appendChild(warningBox);
    document.body.appendChild(warningOverlay);

    document.getElementById('closeMobileWarning').addEventListener('click', () => {
      warningOverlay.style.opacity = '0';
      warningOverlay.style.transition = 'opacity 0.4s ease';
      setTimeout(() => {
        warningOverlay.remove();
      }, 400);
      sessionStorage.setItem('mobile_warning_seen', 'true');
    });
  }

});
