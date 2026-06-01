
    // Dynamically build the table and Setup Live Search/Filter
    document.addEventListener('DOMContentLoaded', () => {
      
      const tbody = document.getElementById('directoryBody');
      const searchInput = document.getElementById('searchInput');
      const roleFilter = document.getElementById('roleFilter');
      const noResults = document.getElementById('noResults');
      
      window.activeDistrict = 'ALL';
      window.activeCity = 'ALL';
      
      // Build cd15List and cd28List synchronously from precinctDistricts
      window.cd15List = precinctDistricts.filter(p => p.CD === '15' || p.CD === '15, 28' || p.CD === '28, 15').map(p => parseInt(p.PRECINCT, 10));
      window.cd28List = precinctDistricts.filter(p => p.CD === '28' || p.CD === '15, 28' || p.CD === '28, 15').map(p => parseInt(p.PRECINCT, 10));

      // Populate table immediately without fetch to avoid CORS file:// issues
      chairDataList.forEach(person => {
          const row = document.createElement('tr');
          row.className = 'directory-row';
          row.dataset.precinct = person.precinct;
          row.dataset.name = person.name.toLowerCase();
          row.dataset.role = person.role.toLowerCase();

          const badgeClass = person.role === 'Block Captain' ? 'badge-captain' : 'badge-chair';

          row.innerHTML = `
              <td>
                  <span class="pct-badge">${person.precinct}</span>
                  ${(window.cd15List.includes(parseInt(person.precinct)) && window.cd28List.includes(parseInt(person.precinct))) ? '<br><span style="background:#ea580c; color:white; font-size:0.7rem; font-weight: bold; padding: 2px 6px; border-radius: 4px; display:inline-block; margin-top: 5px;">Split District</span>' : ''}
              </td>
              <td class="name-cell">
                  <strong>${person.name}</strong>
                  <div style="font-size: 0.85rem; color: #94a3b8; margin-top: 4px; display: flex; flex-direction: column; gap: 2px;">
                      ${person.email && person.email.toLowerCase() !== 'no email' ? `<span>✉️ <a style="color: #94a3b8; text-decoration: none;" href="mailto:${person.email}">${person.email}</a></span>` : ''}
                      ${person.phone && person.phone.trim() !== '' ? `<span>📞 <a style="color: #94a3b8; text-decoration: none;" href="tel:${person.phone}">${person.phone}</a></span>` : ''}
                  </div>
                  ${person.city ? `<div style="font-size: 0.8rem; color: #64748b; margin-top: 2px;">📍 ${person.city}</div>` : ''}
              </td>
              <td><span class="role-badge ${badgeClass}">${person.role}</span></td>
              <td class="action-cell">
                 <a href="mailto:${person.email}" class="btn btn-sm btn-outline">Contact</a>
              </td>
          `;
          tbody.appendChild(row);
      });

      const rows = document.querySelectorAll('.directory-row');

      function filterTable() {
            const searchTerm = searchInput.value.toLowerCase().trim();
            const roleTerm = roleFilter.value;
            let visibleCount = 0;
            let visiblePrecincts = new Set();

            rows.forEach(row => {
              const name = row.dataset.name;
              const pct = row.dataset.precinct;
              const role = row.dataset.role;
              const pctInt = parseInt(pct, 10);
              
              const matchesSearch = name.includes(searchTerm) || pct === searchTerm;
              const matchesRole = roleTerm === 'all' || 
                                 (roleTerm === 'chair' && role.includes('precinct chair')) ||
                                 (roleTerm === 'captain' && role.includes('block captain'));
                                 
              let matchesDistrict = true;
              if (window.activeDistrict === '15') matchesDistrict = window.cd15List.includes(pctInt);
              if (window.activeDistrict === '28') matchesDistrict = window.cd28List.includes(pctInt);

              let matchesCity = true;
              if (window.activeCity !== 'ALL') {
                  const precinctMapData = precinctDistricts.find(p => parseInt(p.PRECINCT, 10) === pctInt);
                  if (precinctMapData) {
                      matchesCity = (precinctMapData.CITY === window.activeCity);
                  } else {
                      matchesCity = false;
                  }
              }

              if (matchesSearch && matchesRole && matchesDistrict && matchesCity) {
                row.style.display = '';
                visibleCount++;
                visiblePrecincts.add(pct);
              } else {
                row.style.display = 'none';
              }
            });

            noResults.style.display = visibleCount === 0 ? 'block' : 'none';

            if (window.updateMapFromSearch) {
                window.updateMapFromSearch(Array.from(visiblePrecincts), searchTerm);
            }
          }

          // Bind CD buttons
          const cdBtns = document.querySelectorAll('.cd-filter-btn');
          cdBtns.forEach(btn => {
              btn.addEventListener('click', () => {
                  window.activeDistrict = btn.dataset.district;
                  // Reset styling
                  cdBtns.forEach(b => {
                      b.style.background = 'rgba(255,255,255,0.05)';
                      b.style.color = '#94a3b8';
                      b.style.borderColor = 'rgba(255,255,255,0.1)';
                      b.style.boxShadow = 'none';
                  });
                  // Activate selected
                  btn.style.background = 'var(--accent)';
                  btn.style.color = '#020617';
                  btn.style.borderColor = 'var(--accent)';
                  btn.style.boxShadow = '0 0 15px rgba(56,189,248,0.4)';
                  filterTable();
                  if(window.updateMapFromFilters) window.updateMapFromFilters();
              });
          });

          // Bind City buttons
          const cityBtns = document.querySelectorAll('.city-filter-btn');
          cityBtns.forEach(btn => {
              btn.addEventListener('click', () => {
                  window.activeCity = btn.dataset.city;
                  // Reset styling
                  cityBtns.forEach(b => {
                      b.style.background = 'rgba(255,255,255,0.05)';
                      b.style.color = '#94a3b8';
                      b.style.borderColor = 'rgba(255,255,255,0.1)';
                      b.style.boxShadow = 'none';
                  });
                  // Activate selected
                  btn.style.background = 'var(--accent)';
                  btn.style.color = '#020617';
                  btn.style.borderColor = 'var(--accent)';
                  btn.style.boxShadow = '0 0 15px rgba(56,189,248,0.4)';
                  filterTable();
                  if(window.updateMapFromFilters) window.updateMapFromFilters();
              });
          });

          searchInput.addEventListener('input', filterTable);
          roleFilter.addEventListener('change', filterTable);
          filterTable();
          
          // Password protection logic
          const btnUnlock = document.getElementById('btn-unlock');
          const inputPassword = document.getElementById('chair-password');
          const errorMsg = document.getElementById('password-error');
          const overlay = document.getElementById('password-overlay');
          const protectedContent = document.getElementById('protected-content');
          
          const attemptUnlock = () => {
              if (inputPassword.value === 'ddddddd') {
                  overlay.style.display = 'none';
                  protectedContent.style.filter = 'none';
                  protectedContent.style.pointerEvents = 'auto';
                  protectedContent.style.userSelect = 'auto';
              } else {
                  errorMsg.style.display = 'block';
              }
          };
          
          btnUnlock.addEventListener('click', attemptUnlock);
          inputPassword.addEventListener('keypress', (e) => {
              if (e.key === 'Enter') attemptUnlock();
          });
    });
  