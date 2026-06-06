from bs4 import BeautifulSoup
import os

with open('vdr_portal.html', 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f, 'html.parser')

# Update title
title = soup.find('title')
if title:
    title.string = "Voter Registration Tracker | Hidalgo Democrats"

# Add Chart.js to head
head = soup.find('head')
if head:
    chart_script = soup.new_tag('script', src="https://cdn.jsdelivr.net/npm/chart.js")
    head.append(chart_script)
    data_script = soup.new_tag('script', src="js/voter_reg_data.js")
    head.append(data_script)

# Replace the hero section
hero = soup.find('header', class_='civics-hero')
if hero:
    hero.clear()
    h1 = soup.new_tag('h1')
    h1.string = "Voter Registration Goals"
    p = soup.new_tag('p')
    p.string = "Tracking our progress towards a historic turnout in Hidalgo County."
    hero.append(h1)
    hero.append(p)

# Replace main container
main = soup.find('main', class_='civics-container')
if main:
    main.clear()
    
    # Breadcrumbs
    nav_bc = soup.new_tag('nav', attrs={'class': 'breadcrumbs fade-in'})
    a_home = soup.new_tag('a', href="home.html")
    a_home.string = "Home"
    nav_bc.append(a_home)
    span_slash = soup.new_tag('span')
    span_slash.string = " / "
    nav_bc.append(span_slash)
    span_curr = soup.new_tag('span', style="color: #fff;")
    span_curr.string = "Voter Tracker"
    nav_bc.append(span_curr)
    main.append(nav_bc)
    
    # Data Tracking Section
    section_tracker = soup.new_tag('div', attrs={'class': 'party-section', 'style': 'margin-top: 2rem;'})
    h2 = soup.new_tag('h2', attrs={'class': 'civics-section-title'})
    h2.string = "Live Goal Tracker"
    section_tracker.append(h2)
    
    # Dashboard Grid
    dash_grid = soup.new_tag('div', style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 2rem; margin-bottom: 2rem;")
    
    # Current Reg Card
    card1 = soup.new_tag('div', attrs={'class': 'civics-card', 'style': 'text-align: center; cursor: default;'})
    c1_title = soup.new_tag('h3', style="color: #94a3b8;")
    c1_title.string = "Current Registered Voters"
    c1_val = soup.new_tag('div', id="current-count", style="font-size: 3rem; font-weight: 800; color: #38bdf8; font-family: 'Alfa Slab One', cursive;")
    c1_val.string = "---,---"
    card1.append(c1_title)
    card1.append(c1_val)
    dash_grid.append(card1)
    
    # Low Goal Card
    card2 = soup.new_tag('div', attrs={'class': 'civics-card', 'style': 'text-align: center; cursor: default;'})
    c2_title = soup.new_tag('h3', style="color: #94a3b8;")
    c2_title.string = "Baseline Goal (Low)"
    c2_val = soup.new_tag('div', id="low-goal", style="font-size: 3rem; font-weight: 800; color: #f472b6; font-family: 'Alfa Slab One', cursive;")
    c2_val.string = "480,000"
    card2.append(c2_title)
    card2.append(c2_val)
    dash_grid.append(card2)
    
    # High Goal Card
    card3 = soup.new_tag('div', attrs={'class': 'civics-card', 'style': 'text-align: center; cursor: default;'})
    c3_title = soup.new_tag('h3', style="color: #94a3b8;")
    c3_title.string = "Stretch Goal (High)"
    c3_val = soup.new_tag('div', id="high-goal", style="font-size: 3rem; font-weight: 800; color: #34d399; font-family: 'Alfa Slab One', cursive;")
    c3_val.string = "500,000"
    card3.append(c3_title)
    card3.append(c3_val)
    dash_grid.append(card3)
    
    section_tracker.append(dash_grid)
    
    # Graph Container
    graph_container = soup.new_tag('div', style="background: rgba(30, 41, 59, 0.7); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 16px; padding: 2rem; margin-bottom: 2rem; box-shadow: 0 10px 30px rgba(0,0,0,0.2);")
    canvas = soup.new_tag('canvas', id="voterChart", width="400", height="200")
    graph_container.append(canvas)
    section_tracker.append(graph_container)
    
    # Historical Data Table
    table_container = soup.new_tag('div', style="background: rgba(30, 41, 59, 0.7); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 16px; padding: 2rem; margin-bottom: 4rem; box-shadow: 0 10px 30px rgba(0,0,0,0.2); overflow-x: auto;")
    table_title = soup.new_tag('h3', style="color: white; font-family: 'Montserrat', sans-serif; font-size: 1.5rem; margin-bottom: 1.5rem; text-align: center;")
    table_title.string = "Historical Voter Registration Data"
    table_container.append(table_title)
    
    table = soup.new_tag('table', style="width: 100%; border-collapse: collapse; text-align: left;")
    thead = soup.new_tag('thead')
    tr_head = soup.new_tag('tr', style="border-bottom: 2px solid rgba(255,255,255,0.1); color: #94a3b8;")
    for th_text in ["Year", "Election Type", "Registered Voters"]:
        th = soup.new_tag('th', style="padding: 1rem;")
        th.string = th_text
        tr_head.append(th)
    thead.append(tr_head)
    table.append(thead)
    
    tbody = soup.new_tag('tbody', id="historicalDataTableBody")
    table.append(tbody)
    table_container.append(table)
    section_tracker.append(table_container)
    
    main.append(section_tracker)
    
    # VDR Call to action
    vdr_section = soup.new_tag('div', attrs={'class': 'gov-section'})
    h2_vdr = soup.new_tag('h2', attrs={'class': 'civics-section-title'})
    h2_vdr.string = "We Need You To Hit These Goals"
    vdr_section.append(h2_vdr)
    
    vdr_callout = soup.new_tag('div', style="background: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 24px; padding: 3rem 2rem; text-align: center; box-shadow: 0 10px 30px rgba(0,0,0,0.2);")
    v_h3 = soup.new_tag('h3', style="color: #34d399; font-size: 1.75rem; margin-bottom: 1rem; font-family: 'Montserrat', sans-serif; font-weight: 800;")
    v_h3.string = "Become a Volunteer Deputy Registrar"
    v_p = soup.new_tag('p', style="font-size: 1.15rem; line-height: 1.6; color: #cbd5e1; margin-bottom: 2rem; max-width: 800px; margin-left: auto; margin-right: auto;")
    v_p.string = "To hit our 500k stretch goal by the October deadline, we need an army of certified VDRs organizing in their neighborhoods. The party provides the clipboards, the forms, and the training. You provide the boots on the ground."
    v_a = soup.new_tag('a', href="vdr_portal.html", style="display: inline-block; padding: 1rem 3rem; background: linear-gradient(45deg, #34d399, #10b981); color: white; border-radius: 30px; font-family: 'Montserrat', sans-serif; font-weight: 800; font-size: 1.1rem; text-decoration: none; box-shadow: 0 10px 20px rgba(0,0,0,0.3); transition: transform 0.3s ease;")
    v_a.string = "Get Certified Now"
    
    vdr_callout.append(v_h3)
    vdr_callout.append(v_p)
    vdr_callout.append(v_a)
    vdr_section.append(vdr_callout)
    
    main.append(vdr_section)

# Remove the old modal scripts
script_tags = soup.find_all('script')
for script in script_tags:
    if script.string and 'const lessonsData' in script.string:
        script.decompose()

# Inject the Chart script
body = soup.find('body')
if body:
    chart_init = soup.new_tag('script')
    chart_init.string = """
    document.addEventListener('DOMContentLoaded', () => {
      try {
        if (typeof historicalVoterData !== 'undefined' && typeof voterRegistrationData !== 'undefined') {
          // Get historical data for general elections
          const generalElections = historicalVoterData.filter(d => d.type === 'General Election');
          const historicalLabels = generalElections.map(d => d.year.toString());
          const historicalCounts = generalElections.map(d => d.count);
          
          // Get the latest 2026 data
          const currentCount = voterRegistrationData[voterRegistrationData.length - 1].count;
          document.getElementById('current-count').textContent = currentCount.toLocaleString();
          
          // Combine labels and data
          const labels = [...historicalLabels, '2026 (Current)'];
          const data = [...historicalCounts, currentCount];
          
          const chartElement = document.getElementById('voterChart');
          if (chartElement) {
            const ctx = chartElement.getContext('2d');
            
            const lowGoal = typeof voterRegistrationGoals !== 'undefined' ? voterRegistrationGoals.lowGoal : 480000;
            const highGoal = typeof voterRegistrationGoals !== 'undefined' ? voterRegistrationGoals.highGoal : 500000;
            
            // Goals only extend across the whole chart for reference
            const lowGoalData = new Array(labels.length).fill(lowGoal);
            const highGoalData = new Array(labels.length).fill(highGoal);
            
            // Populate the historical data table
            const tbody = document.getElementById('historicalDataTableBody');
            if (tbody) {
              const allData = [...historicalVoterData, { year: 2026, type: 'Current Tracking', count: currentCount }];
              // Sort by year descending
              allData.sort((a, b) => b.year - a.year);
              
              allData.forEach((row, index) => {
                const tr = document.createElement('tr');
                tr.style.borderBottom = '1px solid rgba(255,255,255,0.05)';
                if (index % 2 === 0) tr.style.background = 'rgba(255,255,255,0.02)';
                
                const tdYear = document.createElement('td');
                tdYear.style.padding = '1rem';
                tdYear.style.fontWeight = 'bold';
                tdYear.style.color = '#fff';
                tdYear.textContent = row.year;
                
                const tdType = document.createElement('td');
                tdType.style.padding = '1rem';
                tdType.style.color = '#cbd5e1';
                tdType.textContent = row.type;
                
                const tdCount = document.createElement('td');
                tdCount.style.padding = '1rem';
                tdCount.style.color = '#38bdf8';
                tdCount.style.fontWeight = 'bold';
                tdCount.textContent = row.count.toLocaleString();
                
                tr.appendChild(tdYear);
                tr.appendChild(tdType);
                tr.appendChild(tdCount);
                tbody.appendChild(tr);
              });
            }
            
            new Chart(ctx, {
              type: 'line',
              data: {
                labels: labels,
                datasets: [
                  {
                    label: 'Registered Voters (General Elections)',
                    data: data,
                    borderColor: '#38bdf8',
                    backgroundColor: 'rgba(56, 189, 248, 0.1)',
                    borderWidth: 3,
                    fill: true,
                    tension: 0.1,
                    pointBackgroundColor: function(context) {
                        return context.dataIndex === context.dataset.data.length - 1 ? '#fcd34d' : '#fff';
                    },
                    pointRadius: function(context) {
                        return context.dataIndex === context.dataset.data.length - 1 ? 8 : 5;
                    }
                  },
                  {
                    label: 'Baseline Goal (' + (lowGoal/1000) + 'k)',
                    data: lowGoalData,
                    borderColor: '#f472b6',
                    borderWidth: 2,
                    borderDash: [5, 5],
                    fill: false,
                    pointRadius: 0
                  },
                  {
                    label: 'Stretch Goal (' + (highGoal/1000) + 'k)',
                    data: highGoalData,
                    borderColor: '#34d399',
                    borderWidth: 2,
                    borderDash: [5, 5],
                    fill: false,
                    pointRadius: 0
                  }
                ]
              },
              options: {
                responsive: true,
                plugins: {
                  legend: {
                    labels: { color: '#cbd5e1', font: { family: 'Inter' } }
                  },
                  tooltip: {
                      callbacks: {
                          label: function(context) {
                              let label = context.dataset.label || '';
                              if (label) {
                                  label += ': ';
                              }
                              if (context.parsed.y !== null) {
                                  label += new Intl.NumberFormat('en-US').format(context.parsed.y);
                              }
                              return label;
                          }
                      }
                  }
                },
                scales: {
                  y: {
                    min: 250000,
                    max: 510000,
                    grid: { color: 'rgba(255,255,255,0.05)' },
                    ticks: { 
                        color: '#94a3b8', 
                        font: { family: 'Inter' },
                        callback: function(value, index, values) {
                            return value / 1000 + 'k';
                        }
                    }
                  },
                  x: {
                    grid: { color: 'rgba(255,255,255,0.05)' },
                    ticks: { color: '#94a3b8', font: { family: 'Inter' } }
                  }
                }
              }
            });
          }
        } else {
          console.warn("voter registration data arrays are missing or empty.");
        }
      } catch (e) {
        console.error("Error initializing voter tracker chart:", e);
      }
    });
    """
    body.append(chart_init)

with open('voter_registration_tracker.html', 'w', encoding='utf-8') as f:
    f.write(str(soup))
print("Generated voter_registration_tracker.html successfully.")
