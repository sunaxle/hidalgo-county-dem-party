// news_feed.js
// Fetches the latest political news from an external RSS feed and renders it on the homepage

document.addEventListener("DOMContentLoaded", () => {
    const container = document.getElementById("rss-feed-container");
    if (!container) return;

    // Use rss2json to convert an RSS feed into a JSON response
    // Using the Texas Tribune main feed as the default political news source for Texas Democrats
    const rssUrl = encodeURIComponent("https://www.texastribune.org/feeds/main/");
    const apiUrl = `https://api.rss2json.com/v1/api.json?rss_url=${rssUrl}&api_key=`; 

    fetch(apiUrl)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            if (data.status === 'ok') {
                renderNewsCards(data.items);
            } else {
                throw new Error('Failed to parse RSS feed status');
            }
        })
        .catch(error => {
            console.error("Error fetching RSS feed:", error);
            container.innerHTML = `
                <div class="glass-card" style="text-align: center; padding: 2rem; grid-column: 1 / -1; border-color: rgba(239, 68, 68, 0.3);">
                    <p style="color: #ef4444; margin: 0;">Unable to load the latest news at this time. Please check back later.</p>
                </div>
            `;
        });

    function renderNewsCards(items) {
        // Clear the loading state
        container.innerHTML = '';

        // Only take the first 3 news items to fit perfectly in the grid-3 layout
        const topItems = items.slice(0, 3);

        topItems.forEach((item, index) => {
            // Delay animation based on index
            const delay = index * 0.1;
            
            // Format published date
            const pubDate = new Date(item.pubDate);
            const formattedDate = pubDate.toLocaleDateString("en-US", { 
                month: "short", 
                day: "numeric", 
                year: "numeric" 
            });

            // Extract thumbnail if available. Use a fallback geometry if not.
            let thumbnailHtml = '';
            if (item.thumbnail && item.thumbnail !== "") {
               thumbnailHtml = `<div style="height: 180px; width: 100%; border-radius: 8px 8px 0 0; overflow: hidden; margin: -2rem -2rem 1.5rem -2rem; width: calc(100% + 4rem);">
                                    <img src="${item.thumbnail}" alt="Article Thumbnail" style="width: 100%; height: 100%; object-fit: cover; opacity: 0.8; transition: opacity 0.3s ease;" class="feed-img">
                                </div>`;
            } else {
               // Fallback abstract gradient header for the card
               const gradients = [
                   "linear-gradient(135deg, rgba(34, 211, 238, 0.2), rgba(15, 23, 42, 0.8))",
                   "linear-gradient(135deg, rgba(59, 130, 246, 0.2), rgba(15, 23, 42, 0.8))",
                   "linear-gradient(135deg, rgba(16, 185, 129, 0.2), rgba(15, 23, 42, 0.8))"
               ];
               thumbnailHtml = `<div style="height: 120px; width: 100%; border-radius: 8px 8px 0 0; margin: -2rem -2rem 1.5rem -2rem; width: calc(100% + 4rem); background: ${gradients[index % gradients.length]}; border-bottom: 1px solid rgba(255,255,255,0.05);"></div>`;
            }

            // Create card HTML
            const card = document.createElement("article");
            card.className = "glass-card fade-in feed-card";
            card.style.padding = "2rem";
            card.style.transitionDelay = `${delay}s`;
            card.style.display = "flex";
            card.style.flexDirection = "column";
            card.style.height = "100%";
            card.style.position = "relative"; // needed if hover effects are added

            // Clean description (remove html tags if any)
            let rawDesc = item.description || "";
            // regex to strip html tags for cleaner excerpts
            let cleanDesc = rawDesc.replace(/<[^>]*>?/gm, '');
            // truncate excerpt
            if (cleanDesc.length > 140) cleanDesc = cleanDesc.substring(0, 140) + "...";

            card.innerHTML = `
                ${thumbnailHtml}
                <div style="font-size: 0.75rem; color: var(--accent); font-weight: bold; text-transform: uppercase; margin-bottom: 0.5rem; letter-spacing: 1px; display: flex; justify-content: space-between;">
                    <span>Texas Tribune</span>
                    <span style="color: #94a3b8;">${formattedDate}</span>
                </div>
                <h3 style="margin-bottom: 1rem; line-height: 1.3; font-size: 1.15rem;">
                    <a href="${item.link}" target="_blank" rel="noopener" style="color: #fff; text-decoration: none;" class="feed-link">${item.title}</a>
                </h3>
                <p style="color: var(--text-muted); font-size: 0.9rem; margin-bottom: 1.5rem; flex-grow: 1;">
                    ${cleanDesc}
                </p>
                <a href="${item.link}" target="_blank" rel="noopener" class="btn btn-sm btn-outline" style="align-self: flex-start; margin-top: auto; width: 100%; text-align: center;">Read Full Article</a>
            `;

            // Hover effects handled via JS instead of CSS to avoid creating a new file
            card.addEventListener('mouseenter', () => {
                const img = card.querySelector('.feed-img');
                if (img) img.style.opacity = '1';
                card.style.borderColor = 'rgba(34, 211, 238, 0.4)';
                card.style.transform = 'translateY(-5px)';
            });
            card.addEventListener('mouseleave', () => {
                const img = card.querySelector('.feed-img');
                if (img) img.style.opacity = '0.8';
                card.style.borderColor = 'var(--glass-border)';
                card.style.transform = 'translateY(0)';
            });

            container.appendChild(card);
        });
    }
});
