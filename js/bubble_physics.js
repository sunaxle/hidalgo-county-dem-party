function initBubblePhysics() {
    // 1. Parse active chairs from the selected chairDataList toggle
    // We filter out any items without a valid precinct number, and grab the first chair found per precinct
    const activeNodes = [];
    const seenPrecincts = new Set();
    
    chairDataList.forEach(item => {
      const pct = parseInt(item.precinct);
      if (!isNaN(pct) && !seenPrecincts.has(pct)) {
        seenPrecincts.add(pct);
        activeNodes.push({
          precinct: pct,
          chairName: item.name
        });
      }
    });

    // Sort numerically by precinct
    activeNodes.sort((a,b) => a.precinct - b.precinct);
    
    const mockIssues = [
      { category: "Infrastructure", color: "#facc15", stat: "Streetlights", text: "The top issue we hear at the doors is the lack of working streetlights causing safety concerns." },
      { category: "Infrastructure", color: "#facc15", stat: "Potholes", text: "Residents are frustrated with the city patching phase. Coordination between city and county road crews is our top request." },
      { category: "Infrastructure", color: "#facc15", stat: "Drainage", text: "Even light rain floods the corner intersections. We need county drainage bonds prioritized for our neighborhood." },
      { category: "Public Safety", color: "#ef4444", stat: "Stray Dogs", text: "Animal control response times are too slow. Packs of loose dogs are terrifying families walking to school." },
      { category: "Public Safety", color: "#ef4444", stat: "Speeding", text: "We desperately need speed bumps installed near the elementary school drop-off zones." },
      { category: "Economics", color: "#10b981", stat: "Property Taxes", text: "Appraisal hikes are squeezing working class families. We need to educate voters on homestead exemptions." },
      { category: "Logistics", color: "#a855f7", stat: "Polling Access", text: "We need an early voting location re-opened at the community center; transport is too difficult for seniors." }
    ];

    // 2. Generate node data mapped to D3 variables
    const nodes = activeNodes.map(data => {
      // Pick a random primary issue to define the node's category
      const rootIssue = mockIssues[Math.floor(Math.random() * mockIssues.length)];
      
      // Determine volume (1 to 4 issues reported by this chair)
      const issueCount = Math.floor(Math.random() * 4) + 1;
      
      // Calculate a dynamic radius based on the amount of issues
      const calculatedRadius = 80 + (issueCount * 22); 

      return {
        id: `Pct ${data.precinct}`,
        chairName: data.chairName,
        category: rootIssue.category,
        clusterColor: rootIssue.color,
        volume: issueCount,
        stat: rootIssue.stat,
        desc: `${data.chairName} reporting ${issueCount === 1 ? '1 issue' : issueCount + ' issues.'} Primary concern: "${rootIssue.text}"`,
        radius: calculatedRadius
      };
    });

    // 3. Setup D3 Container Target
    const container = d3.select("#bubble-container");
    const containerDOM = document.getElementById('bubble-container');
    const width = containerDOM.clientWidth;
    const height = containerDOM.clientHeight;

    // 4. Initialize Force Simulation
    const simulation = d3.forceSimulation(nodes)
      .force("charge", d3.forceManyBody().strength(15)) // Slight repulsion to keep bubbles from overlapping totally before collision kicks in
      .force("center", d3.forceCenter(width / 2, height / 2)) // Attract nodes to the dead center
      .force("collide", d3.forceCollide().radius(d => d.radius + 8).iterations(3)) // The physical collision geometry preventing overlap (+8px buffer for shadows)
      .force("x", d3.forceX(width / 2).strength(0.06)) // Gravity pulling back to the horizontal center
      .force("y", d3.forceY(height / 2).strength(0.06)); // Gravity pulling back to the vertical center

    // 5. Inject HTML DOM Nodes into the container
    const nodeElements = container.selectAll(".d3-node")
      .data(nodes)
      .enter().append("div")
      .attr("class", "d3-node")
      .style("width", d => (d.radius * 2) + "px")
      .style("height", d => (d.radius * 2) + "px")
      .style("border-color", d => d.clusterColor)
      .style("box-shadow", d => `0 0 10px ${d.clusterColor}40`)
      .call(d3.drag()
        .on("start", dragstarted)
        .on("drag", dragged)
        .on("end", dragended)
      );

    // Inner Title (Pct XX Data)
    nodeElements.append("div")
      .attr("class", "d3-node-title")
      .text(d => d.id);

    // Invisible tooltip hover box
    const nodeInfo = nodeElements.append("div")
      .attr("class", "d3-node-info")
      .style("border-color", d => d.clusterColor); // Match tooltip border exactly to category color

    // Tooltip Statistic Header
    nodeInfo.append("div")
      .attr("class", "d3-info-stat")
      .style("color", d => d.clusterColor)
      .text(d => d.stat);

    // Tooltip Description
    nodeInfo.append("div")
      .attr("class", "d3-info-desc")
      .text(d => d.desc);

    // Re-center logic if user resizes browser window
    window.addEventListener('resize', () => {
       const newW = containerDOM.clientWidth;
       const newH = containerDOM.clientHeight;
       simulation.force("center", d3.forceCenter(newW / 2, newH / 2))
                 .force("x", d3.forceX(newW / 2).strength(0.06))
                 .force("y", d3.forceY(newH / 2).strength(0.06));
       simulation.alpha(0.3).restart();
    });

    // 6. Simulation Tick Update (The Physics loop rendering positions)
    simulation.on("tick", () => {
      nodeElements
        .style("left", d => {
          // Constrain mathematically so they bounce off the walls of the container DIV instead of leaving the map
          d.x = Math.max(d.radius, Math.min(width - d.radius, d.x));
          return d.x + 'px';
        })
        .style("top", d => {
          d.y = Math.max(d.radius, Math.min(height - d.radius, d.y));
          return d.y + 'px';
        });
    });

    // 7. Click & Drag Handlers
    function dragstarted(event, d) {
      if (!event.active) simulation.alphaTarget(0.3).restart();
      d.fx = d.x;
      d.fy = d.y;
      d3.select(this).classed("dragging", true);
    }

    function dragged(event, d) {
      d.fx = event.x;
      d.fy = event.y;
    }

    function dragended(event, d) {
      if (!event.active) simulation.alphaTarget(0);
      d.fx = null;
      d.fy = null;
      d3.select(this).classed("dragging", false);
    }
    // Expose a public API to external HTML buttons for triggering the categorical magnetic fields.
    // If we click "Infrastructure", we pull all matching items up. Everything else gets dropped down.
    window.sortBubbles = function(targetCategory) {
      if (targetCategory === 'All') {
        // Reset to center blob
        simulation.force("y", d3.forceY(height / 2).strength(0.06));
      } else {
        // Split gravitational Y-axis
        simulation.force("y", d3.forceY(d => {
          if (d.category === targetCategory) {
             return height * 0.25; // Pull target up!
          } else {
             return height * 0.85; // Drop everything else down!
          }
        }).strength(0.1)); // Slightly higher strength than normal to break them apart faster
      }
      
      // Kick the simulator so they start moving aggressively
      simulation.alpha(0.8).restart();
    };

    // 8. Calculate and Inject Widget Statistics
    setTimeout(() => {
      if (document.getElementById('stat-total-issues')) {
        let totalIssues = 0;
        let catCounts = { "Infrastructure": 0, "Public Safety": 0, "Economics": 0, "Logistics": 0 };
        
        nodes.forEach(n => {
          totalIssues += n.volume;
          if (catCounts[n.category] !== undefined) {
             catCounts[n.category] += n.volume;
          }
        });
        
        document.getElementById('stat-total-issues').innerText = totalIssues;
        document.getElementById('stat-active-chairs').innerText = nodes.length;
        document.getElementById('stat-infra').innerText = catCounts["Infrastructure"];
        document.getElementById('stat-safety').innerText = catCounts["Public Safety"];
        document.getElementById('stat-econ').innerText = catCounts["Economics"];
        document.getElementById('stat-logic').innerText = catCounts["Logistics"];
      }
    }, 500);
}

// Fire the physics payload only after the DOM has fully parsed and sized the container limits.
document.addEventListener("DOMContentLoaded", initBubblePhysics);
