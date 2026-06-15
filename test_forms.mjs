import { initializeApp } from "firebase/app";
import { getFirestore, collection, addDoc } from "firebase/firestore";

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
const db = getFirestore(app);

const formSubmissionsCollection = collection(db, "form_submissions");

const mockData = [
  {
    source: "Homepage",
    name: "Alex Johnson",
    email: "alex.j@example.com",
    phone: "555-0100",
    message: "This is test #1 from the Homepage form after the new 4-column layout update. I want to see if this message wraps correctly on the new dashboard!"
  },
  {
    source: "Join the Party",
    name: "Maria Garcia",
    email: "maria.g@example.com",
    phone: "555-0101",
    message: "Test #2 from the Join Page. Checking if the 'Source' column properly attributes this back to the Join page instead of 'General Intake'."
  },
  {
    source: "Community Hub Inbox",
    name: "David Smith",
    email: "david.smith@example.com",
    phone: "555-0102",
    message: "Test #3: Issue Type: Voting Accessibility - The new layout looks great in dark mode! Keep up the good work."
  },
  {
    source: "Contact Us",
    name: "Sarah Lee",
    email: "sarah.lee@example.com",
    phone: "555-0103",
    message: "Test #4 from Contact Page. I am verifying that the phone number and email stack nicely in the Contact Info column."
  }
];

async function runTests() {
  console.log("Starting script to inject mock tests...");
  let count = 0;
  for (const data of mockData) {
    try {
      data.timestamp = new Date();
      data.createdAt = new Date().toISOString();
      await addDoc(formSubmissionsCollection, data);
      console.log(`Injected test for: ${data.source}`);
      count++;
    } catch(e) {
      console.error("Error adding document: ", e);
    }
  }
  console.log(`Done. ${count} test documents added. You can now delete this script.`);
  process.exit(0);
}

runTests();
