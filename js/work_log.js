/**
 * work_log.js
 * Handles LocalStorage CRM logic for The Organizer's Ledger
 */

document.addEventListener('DOMContentLoaded', () => {
    const logForm = document.getElementById('work-log-form');
    const taskInput = document.getElementById('task-input');
    const categoryBtns = document.querySelectorAll('.category-btn');
    const isAgentToggle = document.getElementById('is-agent-toggle');
    const timelineContainer = document.getElementById('timeline-container');
    const agentHoursSavedEl = document.getElementById('agent-hours-saved');
    
    let selectedCategory = "🤝 Organizing"; // Default

    // Category Selection
    categoryBtns.forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            // Remove active class from all
            categoryBtns.forEach(b => b.classList.remove('active-category'));
            // Add to clicked
            btn.classList.add('active-category');
            selectedCategory = btn.dataset.category;
        });
    });

    // Load existing logs
    const loadLogs = () => {
        const logs = JSON.parse(localStorage.getItem('hcdp_work_logs')) || [];
        timelineContainer.innerHTML = '';
        
        let agentCount = 0;

        if (logs.length === 0) {
            timelineContainer.innerHTML = '<p style="color: #94a3b8; text-align: center; font-style: italic; margin-top: 2rem;">No entries yet. Log your first hard day of work above!</p>';
        }

        logs.forEach(log => {
            if (log.isAgent) agentCount++;

            const entryHtml = `
                <div class="timeline-entry fade-in" style="background: rgba(30, 41, 59, 0.7); border: 1px solid rgba(255,255,255,0.05); border-left: 4px solid ${getCategoryColor(log.category)}; padding: 1.5rem; border-radius: 8px; margin-bottom: 1rem;">
                    <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 0.5rem;">
                        <span style="font-weight: 800; color: white; display: flex; align-items: center; gap: 0.5rem;">
                            ${log.category}
                            ${log.isAgent ? '<span style="background: linear-gradient(45deg, #a855f7, #3b82f6); color: white; font-size: 0.7rem; padding: 0.2rem 0.5rem; border-radius: 12px; text-transform: uppercase; font-weight: 800; letter-spacing: 1px;">🧠 Swarm Orchestrated</span>' : ''}
                        </span>
                        <span style="color: #94a3b8; font-size: 0.85rem;">${formatDate(log.timestamp)}</span>
                    </div>
                    <p style="color: #cbd5e1; font-size: 1.1rem; line-height: 1.5;">${escapeHtml(log.task)}</p>
                </div>
            `;
            timelineContainer.insertAdjacentHTML('beforeend', entryHtml);
        });

        // Calculate theoretical hours saved (say 1 agent task saves ~1.5 hours of manual work)
        const hoursSaved = (agentCount * 1.5).toFixed(1);
        if(agentHoursSavedEl) agentHoursSavedEl.textContent = `${hoursSaved} hrs`;
    };

    // Save new log
    logForm.addEventListener('submit', (e) => {
        e.preventDefault();
        
        const taskText = taskInput.value.trim();
        if (!taskText) return;

        const newLog = {
            id: Date.now(),
            task: taskText,
            category: selectedCategory,
            isAgent: isAgentToggle.checked,
            timestamp: new Date().toISOString()
        };

        const logs = JSON.parse(localStorage.getItem('hcdp_work_logs')) || [];
        // Add to beginning of array
        logs.unshift(newLog);
        localStorage.setItem('hcdp_work_logs', JSON.stringify(logs));

        // Reset form
        taskInput.value = '';
        isAgentToggle.checked = false;
        
        loadLogs();
    });

    // Helpers
    const getCategoryColor = (cat) => {
        if (cat.includes('Call')) return '#34d399'; // Green
        if (cat.includes('Email')) return '#38bdf8'; // Blue
        if (cat.includes('Verifi')) return '#fcd34d'; // Yellow
        if (cat.includes('Agent')) return '#a855f7'; // Purple
        return '#f472b6'; // Pink for organizing
    };

    const formatDate = (isoString) => {
        const d = new Date(isoString);
        return d.toLocaleDateString('en-US', { month: 'short', day: 'numeric', hour: '2-digit', minute:'2-digit' });
    };

    const escapeHtml = (unsafe) => {
        return unsafe
             .replace(/&/g, "&amp;")
             .replace(/</g, "&lt;")
             .replace(/>/g, "&gt;")
             .replace(/"/g, "&quot;")
             .replace(/'/g, "&#039;");
    };

    // Init
    loadLogs();
});
