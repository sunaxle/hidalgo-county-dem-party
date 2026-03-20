import glob
import os

with open('about.html', 'r', encoding='utf-8') as f:
    html = f.read()

parts = html.split('  <div class="tx-clone-nav-accent-bar"></div>')
top_nav = parts[0] + '  <div class="tx-clone-nav-accent-bar"></div>\n'
footer_split = parts[1].split('<!-- Footer -->')
footer = '<!-- Footer -->' + footer_split[1]

body = """
  <main class="container fade-in" style="padding-top: 120px; padding-bottom: 60px;">
    
    <div style="text-align: center; max-width: 800px; margin: 0 auto 3rem auto;">
      <div style="display:inline-block; background:rgba(34, 211, 238, 0.1); padding:0.5rem 1rem; border-radius:30px; border:1px solid rgba(34, 211, 238, 0.3); color:#38bdf8; font-weight:800; font-size:0.85rem; letter-spacing:1px; text-transform:uppercase; margin-bottom:1rem;">Experimental Beta</div>
      <h1 style="color: var(--accent); font-size: 3rem; margin-bottom: 1rem;">Grassroots Web Chat</h1>
      <p style="color: #cbd5e1; font-size: 1.1rem; line-height: 1.7;">
        Welcome to the sandbox. This is a highly experimental, decentralized public chat forum for our 2,000+ volunteers and Precinct Chairs to rapidly communicate directly with each other. Please note: This is an unmoderated public square. Be respectful and protect your personal privacy.
      </p>
    </div>

    <!-- Chat Interface -->
    <div style="max-width: 800px; margin: 0 auto; background: rgba(15, 23, 42, 0.7); border: 1px solid rgba(56, 189, 248, 0.3); border-radius: 16px; overflow: hidden; box-shadow: 0 10px 40px rgba(0,0,0,0.6); display: flex; flex-direction: column;">
        
        <!-- Chat Header -->
        <div style="background: rgba(15, 23, 42, 0.95); border-bottom: 1px solid rgba(255,255,255,0.1); padding: 1.2rem 2rem; display: flex; align-items: center; justify-content: space-between;">
            <div style="display: flex; align-items: center; gap: 0.8rem;">
                <div style="width: 12px; height: 12px; background: #10b981; border-radius: 50%; box-shadow: 0 0 10px #10b981;"></div>
                <span style="color: #fff; font-weight: bold; font-size: 1.1rem; font-family: 'Inter', sans-serif;">Hidalgo County Live Chat</span>
            </div>
            <div style="color: #94a3b8; font-size: 0.85rem;" id="chat-count">0 Users Online</div>
        </div>

        <!-- Chat Window -->
        <div id="chat-window" style="height: 500px; overflow-y: auto; padding: 2rem; display: flex; flex-direction: column; gap: 1.5rem; background: linear-gradient(180deg, rgba(15,23,42,0.4) 0%, rgba(2,6,23,0.6) 100%);">
            <!-- Messages inject here -->
            <div style="color: #64748b; font-size: 0.9rem; text-align: center; margin-top: 2rem;">Connecting to universal sandbox server...</div>
        </div>

        <!-- Input Area -->
        <div style="background: rgba(30, 41, 59, 0.6); border-top: 1px solid rgba(255,255,255,0.1); padding: 1.5rem 2rem;">
            
            <div style="display: flex; gap: 1rem; margin-bottom: 1rem;">
                <input type="text" id="chat-name" placeholder="Your Name (E.g. Alice - PCT #14)" style="width: 300px; background: rgba(15, 23, 42, 0.8); border: 1px solid rgba(255,255,255,0.2); border-radius: 8px; color: #fff; padding: 0.8rem 1.2rem; font-family: 'Inter', sans-serif; font-size: 1rem; outline: none; transition: border-color 0.2s;">
            </div>

            <div style="display: flex; gap: 1rem;">
                <textarea id="chat-message" placeholder="Type your message here to the county network..." rows="2" style="flex: 1; background: rgba(15, 23, 42, 0.8); border: 1px solid rgba(255,255,255,0.2); border-radius: 8px; color: #fff; padding: 1rem 1.2rem; font-family: 'Inter', sans-serif; font-size: 1rem; resize: none; outline: none; transition: border-color 0.2s;"></textarea>
                <button id="chat-submit" style="background: var(--accent, #38bdf8); color: #020617; border: none; border-radius: 8px; padding: 0 2rem; font-weight: 800; font-size: 1.1rem; cursor: pointer; transition: transform 0.2s, box-shadow 0.2s;">SEND</button>
            </div>
            
            <p style="color: #64748b; font-size: 0.8rem; margin-top: 1rem; text-align: center;">
                By using this chat room, you agree to our <a href="standards.html" style="color: #94a3b8; text-decoration: underline;">Community Standards</a>. No profanity allowed.
            </p>
        </div>

    </div>
  </main>

  <!-- Interactive Sandbox Javascript -->
  <script>
    document.addEventListener("DOMContentLoaded", () => {
        const windowEl = document.getElementById("chat-window");
        const nameInput = document.getElementById("chat-name");
        const msgInput = document.getElementById("chat-message");
        const submitBtn = document.getElementById("chat-submit");
        const countEl = document.getElementById("chat-count");

        // Focus styling
        [nameInput, msgInput].forEach(el => {
            el.addEventListener("focus", () => el.style.borderColor = "var(--accent, #38bdf8)");
            el.addEventListener("blur", () => el.style.borderColor = "rgba(255,255,255,0.2)");
        });

        // Initialize mock state using LocalStorage for the prototype demonstration
        let chatHistory = JSON.parse(localStorage.getItem("hcdp_sandbox_chat")) || [
            {
                name: "System Admin",
                msg: "Welcome to the Hidalgo County Sandbox Chat. This is a live demonstration prototype deployed by the Antigravity Engine.",
                timestamp: new Date().getTime(),
                isSystem: true
            }
        ];

        // Ensure fake active user count is interesting
        countEl.innerText = Math.floor(Math.random() * 45 + 15) + " Active Operators";

        function formatTime(ms) {
            const d = new Date(ms);
            let h = d.getHours();
            let m = d.getMinutes();
            let ampm = h >= 12 ? 'PM' : 'AM';
            h = h % 12;
            h = h ? h : 12;
            m = m < 10 ? '0'+m : m;
            return `${h}:${m} ${ampm}`;
        }

        function renderChat() {
            windowEl.innerHTML = "";
            chatHistory.forEach(data => {
                const bubble = document.createElement("div");
                bubble.style.display = "flex";
                bubble.style.flexDirection = "column";
                bubble.style.maxWidth = "80%";
                
                // Align user messages to the right, system/others to the left
                const isSystem = data.isSystem;
                const isMe = data.name === nameInput.value.trim() && nameInput.value.trim() !== "";
                
                if (isMe) {
                    bubble.style.alignSelf = "flex-end";
                    bubble.innerHTML = `
                        <div style="font-size: 0.8rem; color: #94a3b8; font-weight: 600; margin-bottom: 0.3rem; text-align: right;">${data.name} <span style="font-weight: 400; opacity: 0.6; margin-left: 0.5rem;">${formatTime(data.timestamp)}</span></div>
                        <div style="background: var(--accent, #38bdf8); color: #020617; padding: 1rem 1.2rem; border-radius: 12px 12px 0 12px; font-size: 1.05rem; line-height: 1.5; font-weight: 500; word-wrap: break-word;">
                            ${data.msg}
                        </div>
                    `;
                } else if(isSystem) {
                    bubble.style.alignSelf = "center";
                    bubble.style.maxWidth = "90%";
                    bubble.innerHTML = `
                        <div style="background: rgba(34, 211, 238, 0.1); border: 1px solid rgba(34, 211, 238, 0.3); color: #38bdf8; padding: 0.8rem 1.5rem; border-radius: 8px; font-size: 0.9rem; text-align: center;">
                            <strong>[${formatTime(data.timestamp)}] ${data.name}:</strong> ${data.msg}
                        </div>
                    `;
                } else {
                    bubble.style.alignSelf = "flex-start";
                    bubble.innerHTML = `
                        <div style="font-size: 0.8rem; color: #94a3b8; font-weight: 600; margin-bottom: 0.3rem;"><span style="font-weight: 400; opacity: 0.6; margin-right: 0.5rem;">${formatTime(data.timestamp)}</span> ${data.name}</div>
                        <div style="background: rgba(30, 41, 59, 0.8); border: 1px solid rgba(255,255,255,0.1); color: #e2e8f0; padding: 1rem 1.2rem; border-radius: 12px 12px 12px 0; font-size: 1.05rem; line-height: 1.5; word-wrap: break-word;">
                            ${data.msg}
                        </div>
                    `;
                }
                
                windowEl.appendChild(bubble);
            });
            windowEl.scrollTop = windowEl.scrollHeight;
        }

        renderChat();

        function handleSend() {
            const n = nameInput.value.trim();
            const m = msgInput.value.trim();
            if(!n) {
                alert("Please enter a Name or Precinct title to chat.");
                nameInput.focus();
                return;
            }
            if(!m) return;

            chatHistory.push({
                name: n,
                msg: m,
                timestamp: new Date().getTime(),
                isSystem: false
            });

            // Persist to local cache for overnight viewing
            localStorage.setItem("hcdp_sandbox_chat", JSON.stringify(chatHistory));

            msgInput.value = "";
            renderChat();

            // Simulate a fake "reply" 3 seconds later so the sandbox feels alive for the prototype
            if (chatHistory.length % 3 === 0) {
                 setTimeout(() => {
                     chatHistory.push({
                         name: "Auto-Responder Bot",
                         msg: "That's a great point, " + n + ". I am an automated sandbox script confirming your message was received by the DOM structure!",
                         timestamp: new Date().getTime(),
                         isSystem: false
                     });
                     localStorage.setItem("hcdp_sandbox_chat", JSON.stringify(chatHistory));
                     renderChat();
                 }, 2500);
            }
        }

        submitBtn.addEventListener("click", handleSend);
        
        msgInput.addEventListener("keydown", (e) => {
            if(e.key === "Enter" && !e.shiftKey) {
                e.preventDefault();
                handleSend();
            }
        });
    });
  </script>
"""

chat_page = top_nav.replace("<title>Who We Are", "<title>Live Chat | Project Sandbox") + body + footer

with open('chat.html', 'w', encoding='utf-8') as f:
    f.write(chat_page)
print("Created chat.html")

modified_count = 0
for filename in glob.glob('*.html'):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Inject into Community Dropdown, under 'Social Wall'
    if "chat.html" not in content and '<a href="social_wall.html">Social Wall</a>' in content:
        content = content.replace(
            '<a href="social_wall.html">Social Wall</a>', 
            '<a href="chat.html" style="color: #2dd4bf; font-weight: 800;">Grassroots Live Chat ⚡</a>\\n            <a href="social_wall.html">Social Wall</a>'
        )
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        modified_count += 1

print(f"Injected Sandbox Chat into {modified_count} navigation menus.")
