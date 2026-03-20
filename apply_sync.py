import re

def update_precinct_js():
    p = "js/precinct.js"
    with open(p, "r", encoding="utf-8") as f:
        c = f.read()

    old_block = """        .then(data => {
            const precinctData = data[precinctId];

            if (precinctData) {
                // 3. Inject the info into the HTML template
                populatePage(precinctData);
            } else {"""
            
    new_block = """        .then(async data => {
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
            } else {"""

    c = c.replace(old_block, new_block)
    with open(p, "w", encoding="utf-8") as f:
        f.write(c)

def update_completion_js():
    p = "js/precinct_completion.js"
    with open(p, "r", encoding="utf-8") as f:
        c = f.read()

    detector_code = """
    // 8. The Volunteer Alert Detector
    if(window.fetchVolunteerData) {
        window.fetchVolunteerData().then(volunteers => {
            const generalVols = volunteers.filter(v => v["Role"].trim() === "General Volunteer");
            
            const matches = [];
            generalVols.forEach(v => {
                const pNum = parseInt(v["Precinct Number"], 10);
                if(vacantPrecincts.some(gap => gap.precinct === pNum)) {
                    matches.push(v);
                    
                    const chips = document.querySelectorAll('.chip');
                    chips.forEach(chip => {
                        if(chip.innerText === "Pct " + pNum) {
                            chip.style.backgroundColor = "#fbbf24";
                            chip.style.color = "#000";
                            chip.style.border = "2px solid #b45309";
                            chip.innerHTML = "⭐ Pct " + pNum + " (Vol Available!)";
                        }
                    });
                }
            });

            if(matches.length > 0) {
                const alertBox = document.createElement("div");
                alertBox.style = "background: rgba(251, 191, 36, 0.15); border: 2px solid #fbbf24; color: #fcd34d; padding: 1.5rem; border-radius: 8px; margin-bottom: 2.5rem; text-align: center; font-size: 1.1rem;";
                alertBox.innerHTML = `<strong>🚨 URGENT:</strong> You have ${matches.length} General Volunteer(s) residing in completely vacant precincts! <br>Contact them via the Portal to promote them to Block Captains.`;
                
                const container = document.querySelector('.container') || document.body;
                container.prepend(alertBox);
            }
        });
    }
});
"""
    c = c.replace("});", detector_code, 1) # Note: replaces the very last }); of the DOMContentLoaded block

    with open(p, "w", encoding="utf-8") as f:
        f.write(c)

if __name__ == "__main__":
    update_precinct_js()
    update_completion_js()
    print("JS logic applied successfully.")
