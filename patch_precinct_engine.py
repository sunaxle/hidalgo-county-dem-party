import re

p = "js/precinct.js"
with open(p, "r", encoding="utf-8") as f:
    c = f.read()

old_block = """        .then(async data => {
            let precinctData = data[precinctId];

            if (precinctData) {
                // Overlay live CSV Data
                if(window.fetchVolunteerData) {
                    try {
                        const csvData = await window.fetchVolunteerData();
                        const liveProfile = csvData.find(d => String(d["Precinct Number"]) === precinctId && (d["Role"].trim() === "Precinct Chair" || d["Role"].trim() === "Block Captain"));
                        if(liveProfile) {
                            precinctData.chair_name = liveProfile["First Name"] + " " + liveProfile["Last Name"];
                            precinctData.bio = liveProfile["Short Bio"];
                            precinctData.email = liveProfile["Email"];
                            precinctData.phone = liveProfile["Phone"];
                            if(liveProfile["Photo Link"] && liveProfile["Photo Link"].trim() !== "") {
                                precinctData.photo_url = liveProfile["Photo Link"].trim();
                            } else {
                                precinctData.photo_url = "https://upload.wikimedia.org/wikipedia/commons/7/7c/Profile_avatar_placeholder_large.png";
                            }
                        }
                    } catch(e) {}
                }
                
                // 3. Inject the info into the HTML template
                populatePage(precinctData);
            } else {
                showError(`Oops! We couldn't find data for Precinct ${precinctId}.`);
            }
        })"""

new_block = """        .then(async data => {
            let precinctData = data[precinctId] || null;

            // Overlay live CSV Data
            if(window.fetchVolunteerData) {
                try {
                    const csvData = await window.fetchVolunteerData();
                    const liveProfile = csvData.find(d => String(d["Precinct Number"]) === precinctId && (d["Role"].trim() === "Precinct Chair" || d["Role"].trim() === "Block Captain"));
                    
                    if(liveProfile) {
                        // If it doesn't exist in JSON, instantiate it dynamically to ensure the profile renders!
                        if (!precinctData) {
                            precinctData = { 
                                precinct: precinctId, 
                                announcement: "Welcome to our new precinct page! Check back soon for localized updates.", 
                                meeting_time: "To Be Announced", 
                                meeting_location: "To Be Announced", 
                                social: {} 
                            };
                        }
                        
                        precinctData.chair_name = liveProfile["First Name"] + " " + liveProfile["Last Name"];
                        precinctData.bio = liveProfile["Short Bio"];
                        precinctData.email = liveProfile["Email"];
                        precinctData.phone = liveProfile["Phone"];
                        if(liveProfile["Photo Link"] && liveProfile["Photo Link"].trim() !== "") {
                            precinctData.photo_url = liveProfile["Photo Link"].trim();
                        } else {
                            precinctData.photo_url = "https://upload.wikimedia.org/wikipedia/commons/7/7c/Profile_avatar_placeholder_large.png";
                        }
                    }
                } catch(e) {}
            }
            
            // 3. Inject the info into the HTML template
            if (precinctData) {
                populatePage(precinctData);
            } else {
                showError(`Oops! We couldn't find data for Precinct ${precinctId}.`);
            }
        })"""

c = c.replace(old_block, new_block)

with open(p, "w", encoding="utf-8") as f:
    f.write(c)

print("Engine logic updated successfully.")
