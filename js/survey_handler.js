/**
 * survey_handler.js
 * 
 * Handles the Master Volunteer Shift Survey form submission.
 * Packages the data into a JSON payload for easy transmission to a Google Apps Script Web App
 * or webhook (e.g. Zapier) to populate a Google Sheet.
 */

document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('master-survey-form');
  const submitBtn = document.getElementById('submit-btn');
  const successBanner = document.getElementById('success-banner');

  if (!form) return;

  form.addEventListener('submit', async (e) => {
    e.preventDefault();

    // 1. UI Loading State
    submitBtn.classList.add('loading');
    submitBtn.disabled = true;
    submitBtn.querySelector('.btn-text').innerText = "Syncing with Database...";

    // 2. Gather form data
    const formData = new FormData(form);
    
    // Function to get all checked values for a group of checkboxes
    const getCheckedValues = (name) => {
      const checked = form.querySelectorAll(`input[name="${name}"]:checked`);
      return Array.from(checked).map(cb => cb.value).join(', ');
    };

    // Build the payload mapping for the Google Sheet / VAN integration
    const payload = {
      timestamp: new Date().toISOString(),
      submitter_type: formData.get('submitter_type') || 'Self',
      first_name: formData.get('first_name') || '',
      last_name: formData.get('last_name') || '',
      email: formData.get('email') || '',
      phone: formData.get('phone') || '',
      precinct: formData.get('precinct') || '',
      best_time_to_contact: formData.get('best_time') || '',
      preferred_contact_method: formData.get('preferred_contact') || '',
      ethnicity: formData.get('ethnicity') || '',
      top_issues: getCheckedValues('issues[]'),
      is_teacher: formData.get('is_teacher') || 'No',
      target_campaigns: getCheckedValues('target_campaigns[]'),
      other_campaigns: formData.get('other_campaigns') || '',
      volunteer_actions: getCheckedValues('volunteer_actions[]'),
      shift_availability: getCheckedValues('shifts[]'),
      open_feedback: formData.get('open_feedback') || ''
    };

    // Print payload to console for debugging/demo
    console.log("🚀 Payload ready for Google Sheets Webhook / VAN Bulk Upload:");
    console.table(payload);

    // 3. Send POST Request to Google Apps Script Webhook
    const WEBHOOK_URL = 'https://script.google.com/macros/s/AKfycbwPi82fwnMQxQjuw961LgB7UXQ8tB5_KJsdyM2cxKbXrAWM13-Ylrgm7Nz6H3a7MIge/exec';
    
    try {
      await fetch(WEBHOOK_URL, {
        method: 'POST',
        mode: 'no-cors', // Needed for unauthenticated Google Apps Script endpoints
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
      });
      
      // Hide form
      form.style.display = 'none';
      
      // Show success banner
      successBanner.style.display = 'block';
      successBanner.scrollIntoView({ behavior: 'smooth', block: 'center' });
      
    } catch (err) {
      console.error("Error submitting form", err);
      alert("There was an error connecting to the database. Please try again or email us directly.");
    } finally {
      // Reset button
      submitBtn.classList.remove('loading');
      submitBtn.disabled = false;
      submitBtn.querySelector('.btn-text').innerText = "Submit Volunteer Profile";
    }
  });
});
