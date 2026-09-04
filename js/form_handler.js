import { initializeApp } from "https://www.gstatic.com/firebasejs/10.12.2/firebase-app.js";
import { initializeAppCheck, ReCaptchaV3Provider } from "https://www.gstatic.com/firebasejs/10.12.2/firebase-app-check.js";
import {
  getFirestore,
  collection,
  addDoc,
  serverTimestamp
} from "https://www.gstatic.com/firebasejs/10.12.2/firebase-firestore.js";

// Initialize Firebase
const firebaseConfig = {
  projectId: "hcdp-digital-inbox",
  appId: "1:884194084346:web:ee44e3410c73322a631043",
  storageBucket: "hcdp-digital-inbox.firebasestorage.app",
  apiKey: "AIzaSyBMSgg__pJEm6NESKJe6l72UydEWZpdMhw",
  authDomain: "hcdp-digital-inbox.firebaseapp.com",
  messagingSenderId: "884194084346",
  projectNumber: "884194084346",
};

const app = initializeApp(firebaseConfig);

// Initialize Firebase App Check
const appCheck = initializeAppCheck(app, {
  provider: new ReCaptchaV3Provider('PENDING_RECAPTCHA_V3_SITE_KEY'),
  isTokenAutoRefreshEnabled: true
});

const db = getFirestore(app);

function initForms() {
  const forms = document.querySelectorAll("form");
  console.log("initForms called. Forms found:", forms.length);

  forms.forEach((form) => {
    form.addEventListener("submit", async (e) => {
      e.preventDefault();
      console.log("Form submit event intercepted!");

      // Prevent multiple submissions
      const submitBtn = form.querySelector('button[type="submit"]');
      const originalText = submitBtn.innerText;
      submitBtn.disabled = true;
      submitBtn.innerText = "Sending...";

      try {
        // Identify source page
        let source = "Contact";
        if (window.location.pathname.includes("subscribe"))
          source = "Subscribe";
        else if (window.location.pathname.includes("join"))
          source = "Join the Party";
        else if (
          window.location.pathname.includes("community_intake") ||
          window.location.pathname.includes("community")
        ) {
          if (form.id === "storyForm") source = "Community - Story";
          else if (form.id === "issueForm") source = "Community - Issue";
          else if (form.id === "eventForm") source = "Community - Event";
          else if (form.id === "generalForm") source = "Community - General";
          else source = "Community Inbox";
        }

        // Dynamically concatenate custom fields into the primary 'message' column
        let combinedMessage =
          form.querySelector("#message")?.value ||
          form.querySelector('[name="story_message"]')?.value ||
          form.querySelector('[name="issue_message"]')?.value ||
          form.querySelector('[name="event_message"]')?.value ||
          form.querySelector('[name="general_message"]')?.value ||
          "";

        if (source.startsWith("Community") || source === "Join the Party") {
          let extras = [];
          const title = form.querySelector('[name="story_title"]')?.value;
          const precinct = form.querySelector('[name="precinct"]')?.value;
          const issueType = form.querySelector('[name="issue_type"]')?.value;
          const eventName = form.querySelector('[name="event_name"]')?.value;
          const eventDate = form.querySelector('[name="event_date"]')?.value;
          const subject = form.querySelector('[name="subject"]')?.value;
          const referredBy = form.querySelector('[name="referred_by"]')?.value;

          if (title) extras.push("Story Title: " + title);
          if (precinct) extras.push("Precinct: " + precinct);
          if (issueType) extras.push("Issue Type: " + issueType);
          if (eventName) extras.push("Event Name: " + eventName);
          if (eventDate) extras.push("Event Date: " + eventDate);
          if (subject) extras.push("Subject: " + subject);
          if (referredBy) extras.push("Referred by: " + referredBy);

          if (combinedMessage) extras.push("\nDetails:\n" + combinedMessage);
          combinedMessage = extras.join("\n");
        }

        // Construct Payload cleanly
        const payload = {
          source: source,
          name:
            form.querySelector("#name")?.value ||
            form.querySelector('[name="name"]')?.value ||
            "",
          firstName:
            form.querySelector("#fname")?.value ||
            form.querySelector('[name="fname"]')?.value ||
            "",
          lastName:
            form.querySelector("#lname")?.value ||
            form.querySelector('[name="lname"]')?.value ||
            "",
          email:
            form.querySelector("#email")?.value ||
            form.querySelector('[name="email"]')?.value ||
            "",
          phone:
            form.querySelector("#phone")?.value ||
            form.querySelector('[name="phone"]')?.value ||
            "",
          zipcode:
            form.querySelector("#zipcode")?.value ||
            form.querySelector('[name="zipcode"]')?.value ||
            "",
          message: combinedMessage,

          // Checkboxes (Subscribe Page)
          optInSms: form.querySelector("#check-sms")?.checked || false,
          optInEmail: form.querySelector("#check-email")?.checked || false,
          optInCall: form.querySelector("#check-phone")?.checked || false,
          optInPerson: form.querySelector("#check-in-person")?.checked || false,
          
          timestamp: serverTimestamp()
        };

        // Send to Firebase Firestore
        await addDoc(collection(db, "form_submissions"), payload);

        // Trigger Automated Welcome Email via Firebase Extension
        if (payload.email) {
          try {
            // Fetch the HTML template from our static assets
            const templateRes = await fetch('/emails/welcome.html');
            if (templateRes.ok) {
              let htmlTemplate = await templateRes.text();
              
              // Inject dynamic variables
              const firstName = payload.firstName || payload.name.split(' ')[0] || "Friend";
              htmlTemplate = htmlTemplate.replace(/{{firstName}}/g, firstName);

              // Add to mail collection for the Firebase Extension to process
              await addDoc(collection(db, "mail"), {
                to: payload.email,
                message: {
                  subject: "Welcome to the Party! 🇺🇸",
                  html: htmlTemplate
                }
              });
            } else {
              console.error("Could not fetch welcome email template.");
            }
          } catch(emailErr) {
            console.error("Failed to enqueue welcome email:", emailErr);
            // Non-fatal, we don't want to crash the form submission if email fails
          }
        }

        // Show Success Message natively within the form container
        form.innerHTML = `
            <div style="text-align: center; padding: 3rem 1rem;">
              <div style="font-size: 3rem; margin-bottom: 1rem;">✅</div>
              <h3 style="color: var(--primary); margin-bottom: 1rem;">Success!</h3>
              <p style="color: #666; font-size: 1.1rem; line-height: 1.5;">Your message has been received. Our team will review your submission and reach out shortly.</p>
            </div>
          `;
      } catch (error) {
        console.error("Error submitting form:", error);
        alert(
          "There was a network error sending your message. Please try again later or email us directly.",
        );
        submitBtn.disabled = false;
        submitBtn.innerText = originalText;
      }
    });
  });
}

if (document.readyState === 'loading') {
  document.addEventListener("DOMContentLoaded", initForms);
} else {
  initForms();
}
