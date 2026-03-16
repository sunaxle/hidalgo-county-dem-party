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
          let source = 'Contact';
          if (window.location.pathname.includes('subscribe')) source = 'Subscribe';
          else if (window.location.pathname.includes('community_intake') || window.location.pathname.includes('community')) {
            if (form.id === 'storyForm') source = 'Community - Story';
            else if (form.id === 'issueForm') source = 'Community - Issue';
            else if (form.id === 'eventForm') source = 'Community - Event';
            else if (form.id === 'generalForm') source = 'Community - General';
            else source = 'Community Inbox';
          }
          
          // Dynamically concatenate custom fields into the primary 'message' column for Google Sheets
          let combinedMessage = form.querySelector('#message')?.value || 
                                form.querySelector('[name="story_message"]')?.value || 
                                form.querySelector('[name="issue_message"]')?.value || 
                                form.querySelector('[name="event_message"]')?.value || 
                                form.querySelector('[name="general_message"]')?.value || '';

          if (source.startsWith('Community')) {
            let extras = [];
            const title = form.querySelector('[name="story_title"]')?.value;
            const precinct = form.querySelector('[name="precinct"]')?.value;
            const issueType = form.querySelector('[name="issue_type"]')?.value;
            const eventName = form.querySelector('[name="event_name"]')?.value;
            const eventDate = form.querySelector('[name="event_date"]')?.value;
            const subject = form.querySelector('[name="subject"]')?.value;
            
            if (title) extras.push('Story Title: ' + title);
            if (precinct) extras.push('Precinct: ' + precinct);
            if (issueType) extras.push('Issue Type: ' + issueType);
            if (eventName) extras.push('Event Name: ' + eventName);
            if (eventDate) extras.push('Event Date: ' + eventDate);
            if (subject) extras.push('Subject: ' + subject);
            
            if (combinedMessage) extras.push('\nDetails:\n' + combinedMessage);
            combinedMessage = extras.join('\n');
          }
          
          // Construct Payload cleanly depending on which form was submitted
          const payload = {
            source: source,
            name: form.querySelector('#name')?.value || form.querySelector('[name="name"]')?.value || '',
            firstName: form.querySelector('#fname')?.value || form.querySelector('[name="fname"]')?.value || '',
            lastName: form.querySelector('#lname')?.value || form.querySelector('[name="lname"]')?.value || '',
            email: form.querySelector('#email')?.value || form.querySelector('[name="email"]')?.value || '',
            phone: form.querySelector('#phone')?.value || form.querySelector('[name="phone"]')?.value || '',
            zipcode: form.querySelector('#zipcode')?.value || form.querySelector('[name="zipcode"]')?.value || '',
            message: combinedMessage,
            
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
