let currentSimulation = null;

document.addEventListener("DOMContentLoaded", async () => {
  const searchBtn = document.getElementById("precinct-search-btn");
  const searchInput = document.getElementById("precinct-search-input");
  const errorMsg = document.getElementById("precinct-search-error");
  
  const nameSearchBtn = document.getElementById("name-search-btn");
  const nameSearchInput = document.getElementById("name-search-input");
  const nameErrorMsg = document.getElementById("name-search-error");
  
  // -- Load Congressional Districts --
  let cd15List = [];
  let cd28List = [];
  try {
      const cd15Res = await fetch('data/cd15_precincts.json');
      cd15List = await cd15Res.json();
      const cd28Res = await fetch('data/cd28_precincts.json');
      cd28List = await cd28Res.json();
  } catch(e) { console.error("Filter API Error:", e); }

  // Precinct Box Redirect
  if (searchBtn) {
    searchBtn.addEventListener("click", () => {
      const val = searchInput.value.trim();
      if (!val || val === "" || isNaN(val)) {
        errorMsg.style.display = "block";
        errorMsg.innerText = "Please enter a valid precinct number.";
        return;
      }
      window.location.href = `precinct.html?id=${val}`;
    });
  }

  // Inject D3 node CSS dynamically
  const d3Styles = document.createElement('style');
  d3Styles.innerHTML = `
    .d3-vol-node {
      position: absolute;
      border-radius: 50%;
      background: rgba(15, 23, 42, 0.85);
      border: 2px solid rgba(14, 165, 233, 0.4);
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      cursor: grab;
      transform: translate(-50%, -50%); /* Crucial for D3 centering */
      transition: box-shadow 0.3s ease, border-color 0.3s ease;
      user-select: none;
      z-index: 2;
    }
    .d3-vol-node:hover {
      z-index: 10;
      box-shadow: 0 0 20px rgba(14, 165, 233, 0.8);
      border-color: #38bdf8;
    }
    .d3-vol-node.dragging {
      cursor: grabbing;
      z-index: 50;
      box-shadow: 0 0 30px rgba(14, 165, 233, 1);
      border-color: #38bdf8;
    }
    .vol-initials {
      color: #fff;
      font-weight: 800;
      pointer-events: none;
    }
    .vol-badge {
      font-size: 0.6rem;
      text-transform: uppercase;
      margin-top: 2px;
      pointer-events: none;
    }
    
    .d3-node-info {
      position: absolute;
      top: 100%;
      left: 50%;
      transform: translateX(-50%) translateY(15px);
      width: 200px;
      background: rgba(15, 23, 42, 0.95);
      border: 1px solid #38bdf8;
      border-radius: 8px;
      padding: 1rem;
      box-shadow: 0 10px 30px rgba(0, 0, 0, 0.8);
      opacity: 0;
      visibility: hidden;
      transition: opacity 0.3s ease, transform 0.3s ease;
      pointer-events: none;
      z-index: 100;
      text-align: center;
    }
    .d3-vol-node:hover .d3-node-info {
      opacity: 1;
      visibility: visible;
      transform: translateX(-50%) translateY(5px);
    }
  `;
  document.head.appendChild(d3Styles);

  if (window.fetchVolunteerData) {
    const data = await window.fetchVolunteerData();
    
    // Sort entire database alphabetically by Last Name
    data.sort((a, b) => {
       const aName = a["last_name"] ? a["last_name"].trim().toLowerCase() : "";
       const bName = b["last_name"] ? b["last_name"].trim().toLowerCase() : "";
       return aName.localeCompare(bName);
    });

    const containerDOM = document.getElementById("bubble-container");
    const countDisplay = document.getElementById("total-vol-count");
    if(countDisplay) countDisplay.innerText = data.length.toLocaleString();

    // Reusable Central Render Algorithm for Physics Nodes
    const renderBubbles = (profilesData, titleText = "Grassroots Volunteer Directory") => {
       if (!containerDOM) return;
       // Wipe container and destroy old simulation bindings
       containerDOM.innerHTML = "";
       if (currentSimulation) {
           currentSimulation.stop();
       }
       
       const titleEl = document.getElementById("roster-title");
       if (titleEl) {
           titleEl.innerHTML = `${titleText} (<span id="total-vol-count">${profilesData.length.toLocaleString()}</span>)`;
       }
       
       if (profilesData.length === 0) {
          containerDOM.innerHTML = `<p style="color:#ef4444; text-align:center; padding: 2rem; font-weight: bold; position:absolute; width:100%; margin-top: 20px;">No volunteer found matching query.</p>`;
          return;
       }

       const width = containerDOM.clientWidth || 800;
       const height = containerDOM.clientHeight || 700;

       // Base radius math to scale depending on amount of dots
       // If 1200 nodes (All), we make them tiny (15px) so they fit on screen like a galaxy!
       // If 40 nodes (A), we make them bigger (35px).
       let baseRadius = 40;
       if (profilesData.length > 500) baseRadius = 15;
       else if (profilesData.length > 200) baseRadius = 22;
       else if (profilesData.length > 50) baseRadius = 30;

       // Format node object for D3
       const nodes = profilesData.map((vol, i) => {
           let badgeColor = "#94a3b8";

           let initials = (vol["first_name"] && vol["first_name"].charAt(0) ? vol["first_name"].charAt(0) : "") + 
                          (vol["last_name"] && vol["last_name"].charAt(0) ? vol["last_name"].charAt(0) : "");

           return {
               id: i,
               fname: vol["first_name"] || "",
               lname: vol["last_name"] || "",
               role: "Volunteer",
               zip: vol["zipcode"] || "N/A",
               color: badgeColor,
               initials: initials.toUpperCase(),
               radius: baseRadius + (Math.random() * 8) // Tiny random size jitter
           };
       });

       const container = d3.select("#bubble-container");

       // Initialize Force Simulation
       currentSimulation = d3.forceSimulation(nodes)
         .force("charge", d3.forceManyBody().strength(profilesData.length > 500 ? -2 : 2)) 
         .force("center", d3.forceCenter(width / 2, height / 2))
         .force("collide", d3.forceCollide().radius(d => d.radius + 2).iterations(3))
         .force("x", d3.forceX(width / 2).strength(0.04))
         .force("y", d3.forceY(height / 2).strength(0.04));

       // Inject DOM Nodes
       const nodeElements = container.selectAll(".d3-vol-node")
         .data(nodes)
         .enter().append("div")
         .attr("class", "d3-vol-node")
         .style("width", d => (d.radius * 2) + "px")
         .style("height", d => (d.radius * 2) + "px")
         .style("border-color", d => d.color)
         .call(d3.drag()
            .on("start", dragstarted)
            .on("drag", dragged)
            .on("end", dragended)
         );

       // Text label inside bubble
       nodeElements.append("div")
         .attr("class", "vol-initials")
         .style("font-size", d => (d.radius * 0.6) + "px")
         .text(d => d.initials);

       // Hover tooltip
       const nodeInfo = nodeElements.append("div")
         .attr("class", "d3-node-info");

       nodeInfo.append("strong")
         .style("color", "#fff")
         .style("font-size", "1.1rem")
         .text(d => d.fname + " " + d.lname);

       nodeInfo.append("div")
         .style("color", d => d.color)
         .style("font-weight", "700")
         .style("margin", "0.3rem 0")
         .text(d => d.role);

       nodeInfo.append("div")
         .style("color", "#94a3b8")
         .text(d => "Zip Code: " + d.zip);

       currentSimulation.on("tick", () => {
         nodeElements
           .style("left", d => {
             d.x = Math.max(d.radius, Math.min(width - d.radius, d.x));
             return d.x + 'px';
           })
           .style("top", d => {
             d.y = Math.max(d.radius, Math.min(height - d.radius, d.y));
             return d.y + 'px';
           });
       });

       // Dragging Logic
       function dragstarted(event, d) {
         if (!event.active) currentSimulation.alphaTarget(0.3).restart();
         d.fx = d.x; d.fy = d.y;
         d3.select(this).classed("dragging", true);
       }
       function dragged(event, d) {
         d.fx = event.x; d.fy = event.y;
       }
       function dragended(event, d) {
         if (!event.active) currentSimulation.alphaTarget(0);
         d.fx = null; d.fy = null;
         d3.select(this).classed("dragging", false);
       }
    };

    // Construct Zip Code Master Filter
    const zipCodeFilterDiv = document.getElementById("zipcode-filter");
    if(zipCodeFilterDiv) {
        const uniqueZips = [...new Set(data.map(d => (d.zipcode || "").trim()).filter(z => z !== "" && z.length >= 5))].sort();

        uniqueZips.forEach(zip => {
            const btn = document.createElement("button");
            btn.innerText = zip;
            btn.className = "alphabet-btn zip-btn";
            btn.style.padding = "0.5rem 1rem";
            btn.style.fontSize = "0.9rem";
            btn.onclick = () => {
                document.querySelectorAll(".alphabet-btn").forEach(b => b.classList.remove("active"));
                btn.classList.add("active");
                
                const filtered = data.filter(d => (d.zipcode || "").trim() === zip);
            };
            zipCodeFilterDiv.appendChild(btn);
        });
    }

    // Construct Congressional District Filters
    const cdFilterDiv = document.getElementById("cd-filter");
    if(cdFilterDiv) {
        const createCDBtn = (label, districtStr) => {
            const btn = document.createElement("button");
            btn.innerText = label;
            btn.className = "alphabet-btn cd-btn";
            btn.style.padding = "0.6rem 1.2rem";
            btn.style.fontSize = "0.95rem";
            btn.style.fontWeight = "bold";
            if (districtStr === 'ALL') btn.classList.add("active");

            btn.onclick = () => {
                // Wipe active state on other CD buttons
                document.querySelectorAll(".cd-btn").forEach(b => b.classList.remove("active"));
                btn.classList.add("active");

                // Clear other global filters visually (A-Z and Zip)
                document.querySelectorAll(".zip-btn, [class*='alphabet-btn']:not(.cd-btn)").forEach(b => b.classList.remove("active"));
                
                let filtered = data;
                if (districtStr === '15') {
                    filtered = data.filter(d => {
                        const pctInt = parseInt(d.precinct, 10);
                        return cd15List.includes(pctInt);
                    });
                    renderBubbles(filtered, `Volunteers in Congressional District 15`);
                } else if (districtStr === '28') {
                    filtered = data.filter(d => {
                        const pctInt = parseInt(d.precinct, 10);
                        return cd28List.includes(pctInt);
                    });
                    renderBubbles(filtered, `Volunteers in Congressional District 28`);
                } else {
                    renderBubbles(data, `All County Volunteers (${data.length} Total)`);
                }
            };
            return btn;
        };

        cdFilterDiv.appendChild(createCDBtn("All Districts", "ALL"));
        cdFilterDiv.appendChild(createCDBtn("District 15", "15"));
        cdFilterDiv.appendChild(createCDBtn("District 28", "28"));
    }

    // Construct Alphabet 'Gravity Filter' Bar
    const alphabetFilterDiv = document.getElementById("alphabet-filter");
    if(alphabetFilterDiv) {
        const letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ".split("");
        
        // Default 'A' button will be used initially instead of 'All' to ensure fast load speed,
        // but user specifically requested 'All' function, we supply 'All' as an option.
        const btnAll = document.createElement("button");
        btnAll.innerText = "All (1,200+)";
        btnAll.className = "alphabet-btn";
        btnAll.onclick = () => {
            document.querySelectorAll(".alphabet-btn").forEach(b => b.classList.remove("active"));
            btnAll.classList.add("active");
            renderBubbles(data, "All Grassroots Volunteers");
        };
        alphabetFilterDiv.appendChild(btnAll);

        letters.forEach(letter => {
            const btn = document.createElement("button");
            btn.innerText = letter;
            btn.className = "alphabet-btn";
            btn.onclick = () => {
                document.querySelectorAll(".alphabet-btn").forEach(b => b.classList.remove("active"));
                btn.classList.add("active");
                
                const filtered = data.filter(d => {
                    const ln = d["last_name"] ? d["last_name"].trim().toUpperCase() : "";
                    return ln.startsWith(letter);
                });
                renderBubbles(filtered, `Volunteers: Last Name "${letter}"`);
            };
            alphabetFilterDiv.appendChild(btn);
        });
        
        // Automatically click "A" on initialization to prevent immediate mobile freezing of 1,200 DOM physics nodes
        const aBtn = alphabetFilterDiv.querySelectorAll('.alphabet-btn')[1]; // [0] is All, [1] is A
        if(aBtn) aBtn.click();
    }
    
    // Native Name Search overriding filter
    if (nameSearchBtn) {
        nameSearchBtn.addEventListener("click", () => {
          const val = nameSearchInput.value.trim().toLowerCase();
          if (!val || val === "") {
            nameErrorMsg.style.display = "block";
            nameErrorMsg.innerText = "Please enter a name to search.";
            return;
          }
          nameErrorMsg.style.display = "none";
          
          document.querySelectorAll(".alphabet-btn").forEach(b => b.classList.remove("active"));
          
          const matches = data.filter(d => 
            ((d["first_name"] || "") + " " + (d["last_name"] || "")).toLowerCase().includes(val)
          );
          
          renderBubbles(matches, `Search Results for "${nameSearchInput.value}"`);
        });
    }
  }
});
