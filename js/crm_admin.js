import { initializeApp } from "https://www.gstatic.com/firebasejs/10.12.2/firebase-app.js";
import {
  getFirestore,
  collection,
  query,
  orderBy,
  limit,
  onSnapshot,
  doc,
  setDoc,
  addDoc,
  serverTimestamp
} from "https://www.gstatic.com/firebasejs/10.12.2/firebase-firestore.js";

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

let contactsData = [];
let inboxData = [];
let sortCol = "name";
let sortDir = 1;
let currentTag = "";
let searchTerm = "";

document.addEventListener("DOMContentLoaded", () => {
    // View Toggles
    const btnContacts = document.getElementById("btnContactsView");
    const btnInbox = document.getElementById("btnInboxView");
    const contactsView = document.getElementById("contactsView");
    const inboxView = document.getElementById("inboxView");
    
    if(btnContacts && btnInbox) {
        btnContacts.addEventListener("click", () => {
            btnContacts.classList.add("active-view");
            btnContacts.style.background = "#00ff41";
            btnContacts.style.color = "#000";
            btnInbox.classList.remove("active-view");
            btnInbox.style.background = "transparent";
            btnInbox.style.color = "#00ff41";
            contactsView.style.display = "block";
            inboxView.style.display = "none";
        });
        
        btnInbox.addEventListener("click", () => {
            btnInbox.classList.add("active-view");
            btnInbox.style.background = "#00ff41";
            btnInbox.style.color = "#000";
            btnContacts.classList.remove("active-view");
            btnContacts.style.background = "transparent";
            btnContacts.style.color = "#00ff41";
            inboxView.style.display = "block";
            contactsView.style.display = "none";
        });
    }
    
    // Search Filter
    const searchInput = document.getElementById("searchInput");
    if(searchInput) {
        searchInput.addEventListener("input", (e) => {
            searchTerm = e.target.value.toLowerCase();
            renderContacts();
        });
    }
    
    // Tag Filters
    const tagBtns = document.querySelectorAll("#roleToggles button");
    tagBtns.forEach(btn => {
        btn.addEventListener("click", (e) => {
            tagBtns.forEach(b => {
                b.style.background = "transparent";
                b.style.color = "#00ff41";
            });
            btn.style.background = "#00ff41";
            btn.style.color = "#000";
            currentTag = btn.getAttribute("data-tag") || "";
            renderContacts();
        });
    });
    
    // Contact Form Submission
    const contactForm = document.getElementById("contactForm");
    if(contactForm) {
        contactForm.addEventListener("submit", async (e) => {
            e.preventDefault();
            const id = document.getElementById("contactId").value;
            const payload = {
                firstName: document.getElementById("firstName").value,
                lastName: document.getElementById("lastName").value,
                email: document.getElementById("email").value,
                phone: document.getElementById("phone").value,
                precinct: document.getElementById("precinct").value,
                roles: document.getElementById("roles").value,
                capabilities: document.getElementById("capabilities").value,
                background: document.getElementById("background").value,
                adminNotes: document.getElementById("adminNotes").value,
                updatedAt: serverTimestamp()
            };
            
            try {
                if (!id) {
                    payload.createdAt = serverTimestamp();
                    await addDoc(collection(db, "contacts"), payload);
                } else {
                    await setDoc(doc(db, "contacts", id), payload, { merge: true });
                }
                window.crmApi.closeModal();
            } catch (err) {
                console.error("Error saving contact:", err);
                alert("Failed to save contact. Check permissions.");
            }
        });
    }

    // Load Data Streams
    loadContacts();
    loadInbox();
});

function loadContacts() {
    onSnapshot(collection(db, "contacts"), (snapshot) => {
        contactsData = [];
        snapshot.forEach(doc => {
            contactsData.push({ id: doc.id, ...doc.data() });
        });
        const totalEl = document.getElementById("statTotal");
        if(totalEl) totalEl.innerText = contactsData.length;
        renderContacts();
    }, (error) => {
        console.error("Error fetching contacts:", error);
        const tbody = document.getElementById("contactsTableBody");
        if(tbody) tbody.innerHTML = `<tr><td colspan="5" style="text-align: center; color: #ef4444;">Error loading contacts.</td></tr>`;
    });
}

function loadInbox() {
    const q = query(collection(db, "form_submissions"), orderBy("timestamp", "desc"), limit(100));
    onSnapshot(q, (snapshot) => {
        inboxData = [];
        snapshot.forEach(doc => {
            inboxData.push({ id: doc.id, ...doc.data() });
        });
        const totalEl = document.getElementById("inboxTotal");
        if(totalEl) totalEl.innerText = inboxData.length;
        renderInbox();
    }, (error) => {
        console.error("Error fetching inbox:", error);
        const tbody = document.getElementById("inboxTableBody");
        if(tbody) tbody.innerHTML = `<tr><td colspan="5" style="text-align: center; color: #ef4444;">Error loading messages.</td></tr>`;
    });
}

function renderContacts() {
    let filtered = contactsData.filter(c => {
        let matchSearch = true;
        if (searchTerm) {
            const str = ((c.firstName||"") + " " + (c.lastName||"") + " " + (c.email||"") + " " + (c.phone||"")).toLowerCase();
            matchSearch = str.includes(searchTerm);
        }
        let matchTag = true;
        if (currentTag) {
            matchTag = (c.roles || "").toLowerCase().includes(currentTag.toLowerCase());
        }
        return matchSearch && matchTag;
    });
    
    filtered.sort((a, b) => {
        let valA = a[sortCol] || "";
        let valB = b[sortCol] || "";
        if (sortCol === "name") {
            valA = ((a.firstName||"") + " " + (a.lastName||"")).toLowerCase();
            valB = ((b.firstName||"") + " " + (b.lastName||"")).toLowerCase();
        } else if (sortCol === "contact") {
            valA = (a.email || "").toLowerCase();
            valB = (b.email || "").toLowerCase();
        }
        if (valA < valB) return -1 * sortDir;
        if (valA > valB) return 1 * sortDir;
        return 0;
    });
    
    const showEl = document.getElementById("statShowing");
    if(showEl) showEl.innerText = filtered.length;
    
    const tbody = document.getElementById("contactsTableBody");
    if(!tbody) return;
    
    tbody.innerHTML = "";
    if (filtered.length === 0) {
        tbody.innerHTML = `<tr><td colspan="5" style="text-align: center;">No contacts found.</td></tr>`;
        return;
    }
    
    filtered.forEach(c => {
        const name = `${c.firstName || ""} ${c.lastName || ""}`.trim();
        let tagsHtml = "";
        if (c.roles) {
            c.roles.split(",").forEach(t => {
                const tag = t.trim();
                if (tag) tagsHtml += `<span class="tag">${tag}</span>`;
            });
        }
        
        const tr = document.createElement("tr");
        tr.innerHTML = `
            <td>${name}</td>
            <td>
              <div>${c.email || ""}</div>
              <div>${c.phone || ""}</div>
            </td>
            <td>${c.precinct || ""}</td>
            <td>${tagsHtml}</td>
            <td>
              <button class="btn" onclick="window.crmApi.editContact('${c.id}')">EDIT</button>
            </td>
        `;
        tbody.appendChild(tr);
    });
}

function renderInbox() {
    const tbody = document.getElementById("inboxTableBody");
    if(!tbody) return;
    
    tbody.innerHTML = "";
    if (inboxData.length === 0) {
        tbody.innerHTML = `<tr><td colspan="5" style="text-align: center;">No messages.</td></tr>`;
        return;
    }
    
    inboxData.forEach(m => {
        let dateStr = "";
        if (m.timestamp) dateStr = m.timestamp.toDate().toLocaleString();
        
        const name = m.name || `${m.firstName || ""} ${m.lastName || ""}`.trim() || "Unknown";
        
        const tr = document.createElement("tr");
        tr.innerHTML = `
            <td>${dateStr}</td>
            <td>${name}</td>
            <td>${m.source || ""}</td>
            <td>${(m.message || "").substring(0, 50)}...</td>
            <td>
                <button class="btn" onclick="window.crmApi.viewInbox('${m.id}')">VIEW</button>
            </td>
        `;
        tbody.appendChild(tr);
    });
}

window.crmApi = {
    handleSort: (col) => {
        if (sortCol === col) {
            sortDir = sortDir * -1;
        } else {
            sortCol = col;
            sortDir = 1;
        }
        document.getElementById("sort-name").innerText = "↕";
        document.getElementById("sort-contact").innerText = "↕";
        document.getElementById("sort-precinct").innerText = "↕";
        
        const indicator = sortDir === 1 ? "↓" : "↑";
        const el = document.getElementById(`sort-${col}`);
        if(el) el.innerText = indicator;
        
        renderContacts();
    },
    openModal: () => {
        const form = document.getElementById("contactForm");
        if(form) form.reset();
        document.getElementById("contactId").value = "";
        document.getElementById("modalTitle").innerText = "Add Contact";
        document.getElementById("contactModal").style.display = "flex";
    },
    closeModal: () => {
        document.getElementById("contactModal").style.display = "none";
    },
    editContact: (id) => {
        const c = contactsData.find(x => x.id === id);
        if (!c) return;
        document.getElementById("contactId").value = c.id;
        document.getElementById("firstName").value = c.firstName || "";
        document.getElementById("lastName").value = c.lastName || "";
        document.getElementById("email").value = c.email || "";
        document.getElementById("phone").value = c.phone || "";
        document.getElementById("precinct").value = c.precinct || "";
        document.getElementById("roles").value = c.roles || "";
        document.getElementById("capabilities").value = c.capabilities || "";
        document.getElementById("background").value = c.background || "";
        document.getElementById("adminNotes").value = c.adminNotes || "";
        
        document.getElementById("modalTitle").innerText = "Edit Contact";
        document.getElementById("contactModal").style.display = "flex";
    },
    viewInbox: (id) => {
        const m = inboxData.find(x => x.id === id);
        if (!m) return;
        
        const name = m.name || `${m.firstName || ""} ${m.lastName || ""}`.trim() || "Unknown";
        let dateStr = "";
        if (m.timestamp) dateStr = m.timestamp.toDate().toLocaleString();
        
        document.getElementById("inboxModalSender").innerText = name;
        document.getElementById("inboxModalContact").innerText = `${m.email || ""} | ${m.phone || ""}`;
        document.getElementById("inboxModalSource").innerText = m.source || "";
        document.getElementById("inboxModalDate").innerText = dateStr;
        document.getElementById("inboxModalMessage").innerText = m.message || "";
        
        document.getElementById("inboxModal").style.display = "flex";
    },
    closeInboxModal: () => {
        document.getElementById("inboxModal").style.display = "none";
    }
};
