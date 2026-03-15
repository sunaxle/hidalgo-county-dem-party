// Demographic Map D3 Engine for Hidalgo County
// Simulates a Dot-Density Map for 2026 Electorates

document.addEventListener('DOMContentLoaded', () => {
    const width = window.innerWidth;
    const height = window.innerHeight;

    // Remove loading spinner after initial load wait
    const loadingText = document.getElementById('loading-text');

    // Create the SVG container
    const svg = d3.select("#map-container").append("svg")
        .attr("width", width)
        .attr("height", height)
        .attr("viewBox", [0, 0, width, height]);

    // Add a group for semantic zooming
    const g = svg.append("g");

    // Implement Zoom interaction
    const zoom = d3.zoom()
        .scaleExtent([1, 8]) // Zoom levels: 1x to 8x
        .on("zoom", (event) => {
            g.attr("transform", event.transform);
        });
    svg.call(zoom);

    // Fetch the raw Hidalgo Precinct GeoJSON boundaries
    d3.json("./hidalgo-election-map/hidalgo_precincts.geojson").then(geojson => {
        
        loadingText.innerHTML = "Projecting Geographic Polygons...";

        // 1. Create a Mercator projection tailored to fit Hidalgo County's bounding box onto the screen
        const projection = d3.geoMercator()
            .fitExtent([[50, 50], [width - 50, height - 50]], geojson); // 50px padding

        // 2. Map coordinates -> SVG Path
        const path = d3.geoPath().projection(projection);

        // 3. Draw the base map (Precinct Boundaries)
        g.selectAll("path")
            .data(geojson.features)
            .enter().append("path")
            .attr("d", path)
            .attr("fill", "#050505") // Pitch black void to make dots pop
            .attr("stroke", "#222222") // Faint dark grey borders
            .attr("stroke-width", 0.5);

        loadingText.innerHTML = "Computing Modeled Demographics...";

        // 4. Dot-Density Logic Definition
        const DOT_RATIO = 10; // 1 visually rendered dot = 10 modeled voters
        const dots = [];

        // Texas Demographic Mock Distribution (Hidalgo heavy)
        // Adjusting ratios specifically for South Texas D Primary behavior
        // Approx: 86.8% Hispanic, 9.3% White, 2.1% Black, 1.8% Asian/Other
        
        // Loop over each precinct polygon
        geojson.features.forEach(feature => {
            // Assign a random population between 400 and 1500 for the precinct
            const simulatedVoters = Math.floor(Math.random() * 1100) + 400; 
            const requiredDots = Math.floor(simulatedVoters / DOT_RATIO);

            // Get the geographic Lat/Long bounding box for the specific precinct
            const bounds = d3.geoBounds(feature);
            const lonMin = bounds[0][0]; // Left
            const latMin = bounds[0][1]; // Bottom
            const lonMax = bounds[1][0]; // Right
            const latMax = bounds[1][1]; // Top

            let dotsSpawned = 0;
            let attempts = 0;
            const maxAttempts = requiredDots * 20; // Failsafe to prevent infinite loops on oddly-shaped rural polygons

            // Spawn dots inside the exact mathematical borders
            while (dotsSpawned < requiredDots && attempts < maxAttempts) {
                attempts++;

                // Pick a random Longitude/Latitude strictly within the box
                const randomLon = Math.random() * (lonMax - lonMin) + lonMin;
                const randomLat = Math.random() * (latMax - latMin) + latMin;

                // CRITICAL constraints check: Is this random coordinate mathematically INSIDE the complex polygon shape?
                if (d3.geoContains(feature, [randomLon, randomLat])) {
                    
                    // Assign a demographic color via probability
                    let demo, color;
                    const r = Math.random();
                    if (r < 0.868) { 
                        demo = "Hispanic"; 
                        color = "#ffd700"; // Gold
                    } else if (r < 0.961) { 
                        demo = "White"; 
                        color = "#1e90ff"; // Blue
                    } else if (r < 0.982) { 
                        demo = "Black"; 
                        color = "#32cd32"; // Green
                    } else { 
                        demo = "Asian/Other"; 
                        color = "#ff4500"; // Red
                    }

                    // Store the valid coordinate
                    dots.push({
                        coordinates: [randomLon, randomLat],
                        color: color,
                        demo: demo
                    });
                    
                    dotsSpawned++;
                }
            }
        });

        loadingText.innerHTML = "Rendering Density Clusters...";

        // 5. Render the Dots
        // We render these on top of the paths
        setTimeout(() => {
            g.selectAll("circle")
                .data(dots)
                .enter().append("circle")
                .attr("cx", d => projection(d.coordinates)[0]) // Project Random Lon to SVG X
                .attr("cy", d => projection(d.coordinates)[1]) // Project Random Lat to SVG Y
                .attr("r", 1.0) // Very small dot size
                .attr("fill", d => d.color)
                .attr("opacity", 0.65) // Lower opacity blends dense clusters together
                .style("mix-blend-mode", "screen"); // Forces overlaid colors to glow bright white locally

            // Remove loading screen
            document.getElementById('loading').style.display = 'none';
        }, 300); // Slight delay so the UI thread doesn't fully lock during path injection

    }).catch(error => {
        console.error("Error loading GeoJSON data:", error);
        loadingText.innerHTML = "Error loading spatial matrix.";
        loadingText.style.color = "red";
    });

});
