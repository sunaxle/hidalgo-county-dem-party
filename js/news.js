import { initializeApp } from "https://www.gstatic.com/firebasejs/10.12.2/firebase-app.js";
import { getFirestore, collection, query, orderBy, getDocs } from "https://www.gstatic.com/firebasejs/10.12.2/firebase-firestore.js";

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

document.addEventListener("DOMContentLoaded", async () => {
  const newsFeed = document.getElementById("newsFeed");
  const loadingState = document.getElementById("loadingState");

  try {
    const q = query(collection(db, "seo_articles"), orderBy("timestamp", "desc"));
    const querySnapshot = await getDocs(q);
    
    loadingState.style.display = "none";

    if (querySnapshot.empty) {
      newsFeed.innerHTML = `
        <div style="text-align: center; padding: 4rem; color: #64748b;">
          <h2>No articles published yet.</h2>
          <p>Check back soon for local updates.</p>
        </div>
      `;
      return;
    }

    querySnapshot.forEach((doc) => {
      const article = doc.data();
      const date = article.timestamp ? new Date(article.timestamp).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      }) : 'Recently Published';

      const articleEl = document.createElement("article");
      articleEl.className = "article-card fade-in";
      
      const parsedContent = typeof marked !== 'undefined' ? marked.parse(article.content) : article.content;

      articleEl.innerHTML = `
        <h2 class="article-title">${article.title}</h2>
        <div class="article-meta">Published: ${date}</div>
        <div class="article-content">${parsedContent}</div>
      `;
      
      newsFeed.appendChild(articleEl);
    });

  } catch (error) {
    console.error("Error fetching articles:", error);
    loadingState.style.display = "none";
    newsFeed.innerHTML = `
      <div style="text-align: center; padding: 4rem; color: #ef4444;">
        <h2>Connection Error</h2>
        <p>Failed to load the digital archives. Please refresh the page.</p>
      </div>
    `;
  }
});
