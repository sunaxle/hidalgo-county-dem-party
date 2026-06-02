import { initializeApp } from "https://www.gstatic.com/firebasejs/10.12.2/firebase-app.js";
import { getAuth, signInWithPopup, GoogleAuthProvider, signOut, onAuthStateChanged } from "https://www.gstatic.com/firebasejs/10.12.2/firebase-auth.js";
import { getAnalytics } from "https://www.gstatic.com/firebasejs/10.12.2/firebase-analytics.js";

const firebaseConfig = {
  apiKey: "AIzaSyDntQBIgWoOIBzcN9TzNNL7kkVIKbX_Qeo",
  authDomain: "hcdp-69500.firebaseapp.com",
  projectId: "hcdp-69500",
  storageBucket: "hcdp-69500.firebasestorage.app",
  messagingSenderId: "803078635860",
  appId: "1:803078635860:web:3f475d6d7a2c761b0bc8c1",
  measurementId: "G-SXTQRBQWLM"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);
const auth = getAuth(app);
const provider = new GoogleAuthProvider();

// DOM Elements
document.addEventListener("DOMContentLoaded", () => {
    const loginContainer = document.getElementById("auth-container");
    
    if(!loginContainer) return;

    // Monitor Auth State
    onAuthStateChanged(auth, (user) => {
        if (user) {
            // User is signed in
            loginContainer.innerHTML = `
                <div class="user-profile" style="display: flex; align-items: center; gap: 8px;">
                    <img src="${user.photoURL}" alt="Profile" style="width: 32px; height: 32px; border-radius: 50%; border: 2px solid white;">
                    <button id="btn-logout" class="btn-donate-sm" style="background: #475569;">LOGOUT</button>
                </div>
            `;
            document.getElementById("btn-logout").addEventListener("click", () => {
                signOut(auth);
            });
        } else {
            // User is signed out
            loginContainer.innerHTML = `
                <button id="btn-login" class="btn-donate-sm" style="background: white; color: var(--hcdp-blue); display: flex; align-items: center; gap: 5px;">
                    <svg width="14" height="14" viewBox="0 0 24 24"><path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/><path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/><path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/><path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/></svg>
                    SIGN IN
                </button>
            `;
            document.getElementById("btn-login").addEventListener("click", () => {
                signInWithPopup(auth, provider)
                .then((result) => {
                    console.log("Logged in:", result.user.email);
                }).catch((error) => {
                    console.error("Login failed:", error);
                    alert("Login failed. Please try again.");
                });
            });
        }
    });
});
