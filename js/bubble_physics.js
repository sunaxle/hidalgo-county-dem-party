function initBubblePhysics() {
    // 1. Parse unique filled precincts from chairDataList
    // We filter out any items without a valid precinct number, map to Ints, and remove duplicates.
    const uniquePrecincts = [...new Set(chairDataList.map(item => parseInt(item.precinct)).filter(p => !isNaN(p)))].sort((a,b) => a - b);
    
    const mockIssues = [
      { stat: "Streetlights", desc: "Precinct Chair Report: 'The top issue we hear at the doors is the lack of working streetlights causing safety concerns.'" },
      { stat: "Polling Access", desc: "Precinct Chair Report: 'We need an early voting location re-opened at the community center; transport is too difficult for seniors.'" },
      { stat: "Potholes", desc: "Precinct Chair Report: 'Residents are frustrated with the city patching phase. Coordination between city and county road crews is our top request.'" },
      { stat: "Stray Dogs", desc: "Precinct Chair Report: 'Animal control response times are too slow. Packs of loose dogs are terrifying families walking to school.'" },
      { stat: "Drainage", desc: "Precinct Chair Report: 'Even light rain floods the corner intersections. We need county drainage bonds prioritized for our neighborhood.'" },
      { stat: "Property Taxes", desc: "Precinct Chair Report: 'Appraisal hikes are squeezing working class families. We need to educate voters on homestead exemptions.'" },
      { stat: "Speeding", desc: "Precinct Chair Report: 'We desperately need speed bumps installed near the elementary school drop-off zones.'" }
    ];

    // 2. Generate node data mapped to D3 variables
    const nodes = uniquePrecincts.map(pctNum => {
      const issue = mockIssues[Math.floor(Math.random() * mockIssues.length)];
      return {
        id: `Pct ${pctNum}`,
        stat: issue.stat,
        desc: issue.desc,
        radius: 50 // Represents a 100px diameter CSS width
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
      .attr("class", "d3-node-info");

    // Tooltip Statistic Header
    nodeInfo.append("div")
      .attr("class", "d3-info-stat")
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
}

// Fire the physics payload only after the DOM has fully parsed and sized the container limits.
document.addEventListener("DOMContentLoaded", initBubblePhysics);
