document.addEventListener('DOMContentLoaded', () => {
    // 1. Get the Precinct ID from the URL (e.g., ?id=101)
    const urlParams = new URLSearchParams(window.location.search);
    const precinctId = urlParams.get('id');

    // Default to a generic view or show error if no ID is provided
    if (!precinctId) {
        showError("Welcome! Please select a specific precinct to view their page.");
        return;
    }

    // 2. Fetch the data from the JSON file
    fetch('data/precincts.json')
        .then(response => {
            if (!response.ok) {
                throw new Error("Could not load precinct data.");
            }
            return response.json();
        })
        .then(async data => {
            let precinctData = data[precinctId] || null;

            // Overlay Live Chair Data
            if (typeof chairDataList2026 !== 'undefined') {
                const liveProfile = chairDataList2026.find(d => String(d.precinct) === String(precinctId) && (d.role === "Precinct Chair" || d.role === "Block Captain"));
                if(liveProfile) {
                    if (!precinctData) {
                        precinctData = { 
                            precinct: precinctId, 
                            announcement: "Welcome to our new precinct page! Check back soon for localized updates.", 
                            meeting_time: "To Be Announced", 
                            meeting_location: "To Be Announced", 
                            social: {} 
                        };
                    }
                    
                    precinctData.chair_name = liveProfile.name;
                    precinctData.bio = liveProfile.bio || "Grassroots Leader for Hidalgo County Democrats.";
                    precinctData.email = liveProfile.email;
                    precinctData.phone = liveProfile.phone;
                    precinctData.photo_url = liveProfile.photo || "https://upload.wikimedia.org/wikipedia/commons/7/7c/Profile_avatar_placeholder_large.png";
                }
            }
            
            // NEW LOGIC: Overlay Live Google Forms Data overrides from the user-published CSV
            const GOOGLE_SHEET_CSV = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQl7PmDwc7YoEi0u_lZL1ErXCP03mZhPFhk6--nBynTSn6hahLGaL4nZC0FsfpvAoAPVHU91tp3RVZJ/pub?output=csv";
            
            try {
                if (typeof d3 !== 'undefined') {
                    const liveData = await d3.csv(GOOGLE_SHEET_CSV);
                    const custom_announcements = [];
                    
                    // Parse from oldest to newest entry so multiple update forms stack and merge cumulatively
                    for (let i = 0; i < liveData.length; i++) {
                        const row = liveData[i];
                        const pctKey = "Precinct Number (Critically important, this is how the database knows who is who)";
                        
                        if (String(row[pctKey]).trim() === String(precinctId)) {
                            // Only update non-vital modular fields. 
                            // Official Name and Contact Info are strictly preserved from chair_data.js Native Array.
                            
                            const photoKey = "Profile Picture Link (Have them paste an image URL, or use the Form's File Upload and we'll parse the Google Drive link)";
                            if (row[photoKey] && row[photoKey].trim() !== "") {
                                let cleanMedia = row[photoKey].trim();
                                if(cleanMedia.includes('drive.google.com/file/d/')) {
                                   const idMatch = cleanMedia.match(/file\/d\/(.*?)\/view/);
                                   if(idMatch && idMatch[1]) {
                                      cleanMedia = `https://lh3.googleusercontent.com/d/${idMatch[1]}=w1000`;
                                   }
                                }
                                precinctData.photo_url = cleanMedia;
                            }
                            
                            // Stack announcements instead of overwriting!
                            if (row["Latest Announcement"] && row["Latest Announcement"].trim() !== "") {
                                let block = row["Latest Announcement"].trim();
                                if (row["Timestamp"] && row["Timestamp"].trim() !== "") {
                                    block += `<br><span style="font-size: 0.75rem; color: #94a3b8; font-style: italic;">Posted: ${row["Timestamp"]}</span>`;
                                }
                                custom_announcements.push(block);
                            }
                            
                            // Check if they updated their Biography
                            let bioVal = row["About the Chair"] || row["About the Chair "];
                            if (bioVal && bioVal.trim() !== "") {
                                precinctData.bio = bioVal.trim();
                            }
                            
                            if (row["Next Meeting Time"] && row["Next Meeting Time"].trim() !== "") {
                                precinctData.meeting_time = row["Next Meeting Time"];
                            }
                            if (row["Next Meeting Location"] && row["Next Meeting Location"].trim() !== "") {
                                precinctData.meeting_location = row["Next Meeting Location"];
                            }
                            // Do not break; allow later rows to overwrite earlier rows if they contain new data
                        }
                    }
                    
                    // If we collected custom announcements, stack them visually with newest on top
                    if (custom_announcements.length > 0) {
                        precinctData.announcement_html = custom_announcements.reverse().join('<br><hr style="border:0; border-top:1px dashed #cbd5e1; margin: 12px 0;"><br>');
                    }
                    
                }
            } catch(e) {
                console.warn("Could not load or parse Google Sheet CSV. Reverting to static arrays safely.", e);
            }
            
            // 3. Inject the info into the HTML template
            if (precinctData) {
                populatePage(precinctData);
            } else {
                showError(`Oops! We couldn't find data for Precinct ${precinctId}.`);
            }
        })
        .catch(error => {
            console.error("Error loading precinct data:", error);
            showError("An error occurred while loading this page. Please try again later.");
        });
});

function populatePage(data) {
    // Basic Info
    document.title = `Precinct ${data.precinct} | Hidalgo Democrats`;
    setText('p-number', `Precinct ${data.precinct}`);
    setText('p-name', data.chair_name);
    setText('p-bio', data.bio);
    
    const announcementEl = document.getElementById('p-announcement');
    if (announcementEl) {
        if (data.announcement_html) {
            announcementEl.innerHTML = data.announcement_html;
        } else {
            announcementEl.textContent = data.announcement || '';
        }
    }
    
    setText('p-meeting-time', data.meeting_time);
    setText('p-meeting-location', data.meeting_location);

    // Contact
    const emailEl = document.getElementById('p-email');
    if (emailEl) {
        emailEl.textContent = data.email;
        emailEl.href = `mailto:${data.email}`;
    }
    setText('p-phone', data.phone);

    // Photo
    const photoEl = document.getElementById('p-photo');
    if (photoEl && data.photo_url) {
        photoEl.src = data.photo_url;
        photoEl.alt = `${data.chair_name} - Chair of Precinct ${data.precinct}`;
        
        // Add a safety fallback in case the Chair pastes a broken link or a full webpage URL instead of an image
        photoEl.onerror = function() {
           this.src = "https://upload.wikimedia.org/wikipedia/commons/7/7c/Profile_avatar_placeholder_large.png";
        };
    }

    // Social Links Setup
    const socialContainer = document.getElementById('p-social-links');
    if (socialContainer && data.social) {
        socialContainer.innerHTML = ''; // Clear template
        for (const [network, url] of Object.entries(data.social)) {
            const link = document.createElement('a');
            link.href = url;
            link.className = 'p-social-button';
            link.textContent = capitalize(network);
            socialContainer.appendChild(link);
        }
    }

    // Reveal the content
    document.getElementById('precinct-loading').style.display = 'none';
    document.getElementById('precinct-content').style.display = 'block';
}

function showError(message) {
    document.getElementById('precinct-loading').style.display = 'none';
    const errorEl = document.getElementById('precinct-error');
    errorEl.style.display = 'block';
    errorEl.textContent = message;
}

function setText(id, text) {
    const el = document.getElementById(id);
    if (el) el.textContent = text || '';
}

function capitalize(str) {
    return str.charAt(0).toUpperCase() + str.slice(1);
}
