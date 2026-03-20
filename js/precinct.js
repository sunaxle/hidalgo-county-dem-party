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
        .then(data => {
            const precinctData = data[precinctId];

            if (precinctData) {
                // 3. Inject the info into the HTML template
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
    setText('p-announcement', data.announcement);
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
