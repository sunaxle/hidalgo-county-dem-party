document.addEventListener("DOMContentLoaded", () => {
    // Value Calculation variables
    // Estimating standard agency/freelance rates from 2021-2024 for full stack Web Dev
    const hourlyRate = 85.00; 
    const hoursLogged = 282; // Bumped +4 hours for the global translation MutationObserver and theme swapping logic
    const totalValue = hourlyRate * hoursLogged;

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
            <span style="font-size: 0.8rem; opacity: 0.8;">
                (${hoursLogged} hrs @ $${hourlyRate}/hr)
            </span>
        </div>
    `;

    // Append to the very end of the body
    document.body.appendChild(valueFooter);
});
