document.addEventListener("DOMContentLoaded", () => {
    // Value Calculation variables
    // Estimating standard agency/freelance rates from 2021-2024 for full stack Web Dev
    const standardRate = 85.00;
    const dataRate = 125.00; // Premium rate for data analysis & interactive dataviz
    
    let standardHours = 319.5; // Legacy logged hours
    let dataHours = 0.0;
    
    // Log new sessions
    standardHours += 23.5; // Site-wide template, Dynamic Routing System, Phase 2 Google Sheets CRM
    dataHours += 20.0; // Data Portal maps, Gap Tracker algorithms, D3 Volunteer physics engine
    
    // Recent Work logging (Mar 24)
    standardHours += 32.0; // Mobile Responsiveness UI Audit, Grassroots Chat Upgrades, CRM Pages & Pipeline Dashboard, AI Logos, Theme Customization
    dataHours += 8.0; // Dashboard Data Population, Combining Precinct Data
    
    // April 2026 Operations
    standardHours += 25.0; // Civics Portals, 2026 Roster UI, VDR Partner Integration, Ballot Board Explainer
    dataHours += 15.0; // PII scrubbing algorithms, 2026 data reconciliation pipelines, LUPE Campaign engineering
    
    let totalValue = (standardRate * standardHours) + (dataRate * dataHours);

    // Create the footer element
    const valueFooter = document.createElement("div");
    valueFooter.className = "volunteer-value-banner";
    valueFooter.innerHTML = `
        <div class="volunteer-value-content" style="
            text-align: center; 
            padding: 1rem; 
            background: rgba(15, 23, 42, 0.95); 
            border-top: 1px solid rgba(34, 211, 238, 0.2); 
            color: #cbd5e1; 
            font-size: 0.9rem;
            position: relative;
            z-index: 100;
        ">
            ✨ <strong>In-Kind Volunteer Contribution:</strong> 
            This digital infrastructure was developed by volunteer computer programmers. 
            <br/>
            <span style="color: var(--accent); font-weight: bold; font-size: 1.1rem;">
                Estimated Market Value: $${totalValue.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2})} 
            </span> 
            <span style="font-size: 0.8rem; opacity: 0.8; margin-left: 0.5rem;">
                (${(standardHours + dataHours).toLocaleString()} total hrs)
            </span>
        </div>
    `;

    const sustainingBanner = document.createElement("div");
    sustainingBanner.className = "sustaining-member-banner";
    sustainingBanner.innerHTML = `
        <div style="text-align: center; padding: 2rem 1rem; background: linear-gradient(135deg, #1e3a8a, #0f172a); color: white; border-top: 2px solid var(--accent); position: relative; z-index: 10;">
            <h3 style="margin: 0 0 0.5rem 0; font-size: 1.4rem; color: #fff;">Become a Sustaining Member</h3>
            <p style="margin: 0 auto 1.5rem auto; font-size: 1rem; max-width: 600px; color: #cbd5e1;">
                To keep powering this website, our precinct viewers, and crucial gap trackers, we need your continuous support. Chip in $5 a month to fund this multi-year battle.
            </p>
            <a href="sustaining_members.html" class="btn btn-primary" style="background: var(--accent); color: #020617; font-weight: 800; text-transform: uppercase; letter-spacing: 1px; padding: 0.8rem 2rem; border-radius: 999px; box-shadow: 0 4px 15px rgba(34, 211, 238, 0.4);">Chip In $5/month</a>
        </div>
    `;

    // Append to the very end of the body
    document.body.appendChild(sustainingBanner);
    document.body.appendChild(valueFooter);
});
