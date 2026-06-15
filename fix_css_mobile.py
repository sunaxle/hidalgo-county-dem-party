with open('css/state_party_clone.css', 'a') as f:
    f.write('''
/* --- Ponytail Global Mobile Overrides --- */
@media (max-width: 768px) {
  html, body.tx-clone {
    max-width: 100vw !important;
    overflow-x: hidden !important;
  }
  
  .tx-clone-hero h1 {
    font-size: 2.5rem !important;
  }
  
  .tx-clone-hero-left, .tx-clone-hero-right {
    min-width: 100% !important;
  }
  
  .tx-clone-btn-submit, .tx-clone-btn-donate, .tx-clone-btn-outline {
    min-height: 48px;
    padding: 1rem;
    width: 100%;
    box-sizing: border-box;
    text-align: center;
    display: flex;
    justify-content: center;
    align-items: center;
  }

  .tx-clone-donation-left h2, .tx-clone-content h2 {
    font-size: 2rem !important;
  }

  .tx-clone-grid {
    grid-template-columns: 1fr 1fr !important;
  }
  
  @media (max-width: 480px) {
    .tx-clone-grid {
      grid-template-columns: 1fr !important;
    }
  }
  
  .tx-clone-content p {
    font-size: 1.1rem !important;
  }
  
  .tx-clone-footer {
    padding: 3rem 1rem !important;
  }
}
''')

with open('css/styles.css', 'a') as f:
    f.write('''
/* --- Ponytail Global Mobile Overrides --- */
@media (max-width: 768px) {
  html, body {
    max-width: 100vw !important;
    overflow-x: hidden !important;
  }

  .container {
    padding: 0 1.25rem !important;
  }

  h1 { font-size: 2.2rem !important; }
  h2 { font-size: 1.8rem !important; }
  h3 { font-size: 1.5rem !important; }

  .grid-3, .footer-grid {
    grid-template-columns: 1fr !important;
    gap: 1.5rem !important;
  }

  .form-card, .glass-card {
    padding: 1.5rem !important;
  }

  .btn {
    min-height: 48px;
    width: 100%;
    text-align: center;
    margin-bottom: 0.5rem;
    display: flex;
    justify-content: center;
    align-items: center;
  }

  .hero-actions {
    flex-direction: column;
    width: 100%;
  }

  /* Nav Drawer fixes */
  .nav-links.active {
    width: 100% !important;
    max-width: 100% !important;
    padding-top: 4rem !important;
  }
  
  .dropdown-content {
    min-width: 100% !important;
  }
}
''')

print("CSS files patched.")
