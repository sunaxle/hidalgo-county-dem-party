/**
 * Hidalgo County Democrats - Global Form Handler
 * Captures submissions from Contact and Subscribe pages and routes them to Google Sheets.
 */

document.addEventListener('DOMContentLoaded', () => {
    // We will replace this URL with the live Google Web App URL once generated
    const GOOGLE_WEBHOOK_URL = 'https://script.google.com/macros/s/AKfycbxPJWHK1yEj1Ki6HzgxySr5uRKtJOO-8uN7KcQMDni67s0TbOD0VbOlMqUQPwAn9-jF/exec';
  
    const forms = document.querySelectorAll('form');
  
    forms.forEach(form => {
      form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        // Prevent multiple submissions
        const submitBtn = form.querySelector('button[type="submit"]');
        const originalText = submitBtn.innerText;
        submitBtn.disabled = true;
        submitBtn.innerText = 'Sending...';
        
        try {
          // Identify source page
          const source = window.location.pathname.includes('subscribe') ? 'Subscribe' : 'Contact';
          
          // Construct Payload cleanly depending on which form was submitted
          const payload = {
            source: source,
            name: form.querySelector('#name')?.value || '',
            firstName: form.querySelector('#fname')?.value || '',
            lastName: form.querySelector('#lname')?.value || '',
            email: form.querySelector('#email')?.value || '',
            phone: form.querySelector('#phone')?.value || '',
            zipcode: form.querySelector('#zipcode')?.value || '',
            message: form.querySelector('#message')?.value || '',
            
            // Checkboxes (Subscribe Page)
            optInSms: form.querySelector('#check-sms')?.checked || false,
            optInEmail: form.querySelector('#check-email')?.checked || false,
            optInCall: form.querySelector('#check-phone')?.checked || false,
            optInPerson: form.querySelector('#check-in-person')?.checked || false
          };
  
          // Send to Google Apps Script
          const response = await fetch(GOOGLE_WEBHOOK_URL, {
            method: 'POST',
            mode: 'no-cors', // Google Apps Script requires no-cors for silent POSTs
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
          });
  
          // Show Success Message natively within the form container
          form.innerHTML = `
            <div style="text-align: center; padding: 3rem 1rem;">
              <div style="font-size: 3rem; margin-bottom: 1rem;">✅</div>
              <h3 style="color: var(--primary); margin-bottom: 1rem;">Success!</h3>
              <p style="color: #666; font-size: 1.1rem; line-height: 1.5;">Your message has been received. Our team will review your submission and reach out shortly.</p>
            </div>
          `;
          
        } catch (error) {
          console.error('Error submitting form:', error);
          alert('There was a network error sending your message. Please try again later or email us directly.');
          submitBtn.disabled = false;
          submitBtn.innerText = originalText;
        }
      });
    });
  });
