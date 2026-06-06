import re

with open('press.html', 'r', encoding='utf-8') as f:
    press_html = f.read()

# Extract header
header_match = re.search(r'(.*?<main.*?>)', press_html, re.DOTALL)
footer_match = re.search(r'(</main>.*)', press_html, re.DOTALL)

if header_match and footer_match:
    header = header_match.group(1)
    footer = footer_match.group(1)
    
    # Update title
    header = header.replace('<title>Hidalgo Democrats</title>', '<title>Road to 500k Press Release | Hidalgo Democrats</title>')
    
    content = """
    <div style="background: white; border-radius: 8px; padding: 3rem; margin-top: 2rem; box-shadow: 0 4px 6px rgba(0,0,0,0.05); color: #334155;">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 2rem;">
            <p style="color: #64748b; font-size: 1rem; font-weight: 600;">FOR IMMEDIATE RELEASE • JUNE 5, 2026</p>
            <span style="background: rgba(16, 185, 129, 0.1); color: #10b981; padding: 0.3rem 0.8rem; border-radius: 99px; font-size: 0.8rem; font-weight: 800; letter-spacing: 0.5px;">PRESS RELEASE</span>
        </div>
        
        <h1 style="color: var(--tx-navy); font-size: 2.5rem; margin-bottom: 2rem; line-height: 1.2;">The Road to 500k: The Ultimate Voter Registration Drive</h1>
        
        <p><strong>MEDIA CONTACT:</strong><br>
        Hidalgo County Democratic Party<br>
        <strong>Email:</strong> info@hidalgocountydems.org</p>
        
        <hr style="margin: 2rem 0; border: none; border-top: 2px solid #e2e8f0;">
        
        <p><strong>MEMORANDUM</strong><br>
        <strong>TO:</strong> All Hidalgo County Democratic Party Members, Volunteers, Precinct Chairs, and Supporters<br>
        <strong>FROM:</strong> Richard Gonzalez, Chairman, Hidalgo County Democratic Party<br>
        <strong>SUBJECT:</strong> The Road to 500k: The Ultimate Voter Registration Drive</p>

        <p style="margin-top: 1.5rem; line-height: 1.8;">Hidalgo County is the beating heart of South Texas, and our political power lies in our numbers. Today, we stand at exactly 460,407 registered voters. Through the natural growth of our vibrant community, we net roughly 1,000 new voters each month. With just five months remaining until the October voter registration deadline, organic growth puts us at around 465,000 voters.</p>

        <p style="margin-top: 1rem; line-height: 1.8;">But Democrats do not settle for the status quo. We are built for action, and the stakes for our state are simply too high to leave power on the table.</p>

        <p style="margin-top: 1rem; line-height: 1.8;">That is why today, the Hidalgo County Democratic Party is officially launching the <strong>"Road to 500k" Voter Registration Drive (#RoadTo500k)</strong>.</p>

        <h3 style="margin-top: 2rem; color: var(--tx-navy);">THE NUMBERS:</h3>
        <ul style="margin-top: 1rem; margin-left: 2rem; line-height: 1.8;">
            <li><strong>Current Registered Voters:</strong> 460,407</li>
            <li><strong>Projected Natural Baseline (October):</strong> ~465,000</li>
            <li><strong>Our Baseline Action Goal:</strong> 480,000</li>
            <li><strong>Our Stretch Goal (BHAG):</strong> 500,000</li>
        </ul>

        <p style="margin-top: 1.5rem; line-height: 1.8;">To hit our baseline goal of 480,000 voters, we need our members, precinct chairs, and volunteers to aggressively register at least <strong>15,000 new voters</strong> over the next five months. That means carrying registration cards wherever you go. That means hitting the pavement, knocking on doors, and engaging the unregistered eligible voters in our own neighborhoods.</p>

        <p style="margin-top: 1rem; line-height: 1.8;">But we are a party that dreams bigger. Our Big Hairy Audacious Goal (BHAG) is to cross the threshold of a massive <strong>500,000 registered voters</strong>.</p>

        <p style="margin-top: 1rem; line-height: 1.8;">Reaching half a million registered voters is more than just a milestone. It is an earth-shattering statement. It sends an undeniable message to the rest of Texas that the Rio Grande Valley is organized, mobilized, and ready to determine the future of this state.</p>

        <p style="margin-top: 1rem; line-height: 1.8;">Our community’s future depends on the leaders we elect, and those leaders are chosen by the people who are registered and ready to vote. If we want to defend public education, protect reproductive rights, and build an economy that lifts up working families, we have to expand the electorate.</p>

        <p style="margin-top: 1rem; line-height: 1.8; font-weight: 600; font-size: 1.1rem;">Are you ready to make history?</p>

        <p style="margin-top: 1rem; line-height: 1.8;">Join the Road to 500k today. Step up, get trained as a Volunteer Deputy Registrar, grab a clipboard, and let’s get to work.</p>

        <p style="margin-top: 1rem; line-height: 1.8;">Five months. 15,000 new voters to hit our baseline. Half a million strong to change the state.</p>

        <p style="margin-top: 1rem; line-height: 1.8; font-size: 1.2rem; font-weight: 800; color: var(--tx-navy);">Let’s go.</p>

        <hr style="margin: 2rem 0; border: none; border-top: 2px solid #e2e8f0;">

        <h3 style="color: var(--tx-navy);">INSTRUCTIONS FOR PRECINCT CHAIRS</h3>
        <p style="margin-top: 1rem; line-height: 1.8;">As you mobilize your volunteers and organize your local neighborhood block walks, please ensure all digital and printed outreach materials feature consistent messaging:</p>
        <ol style="margin-top: 1rem; margin-left: 2rem; line-height: 1.8;">
            <li><strong>Unified Hashtag:</strong> Always use <code>#RoadTo500k</code> on social media.</li>
            <li><strong>Branding Elements:</strong> Please use the official graphics below on your personal Facebook and Instagram pages to build momentum.</li>
            <li><strong>Action Link:</strong> Always direct unregistered voters or potential VDRs to our new tracking portal: <a href="voter_registration_tracker.html" style="color: var(--tx-sky); font-weight: bold;">hidalgocountydems.org/voter_registration_tracker.html</a></li>
            <li><strong>VDR Portal:</strong> For all certification resources: <a href="vdr_portal.html" style="color: var(--tx-sky); font-weight: bold;">hidalgocountydems.org/vdr_portal.html</a></li>
        </ol>

        <hr style="margin: 2rem 0; border: none; border-top: 2px solid #e2e8f0;">

        <h3 style="color: var(--tx-navy); margin-bottom: 1.5rem;">OFFICIAL #ROADTO500K MEDIA GRAPHICS</h3>
        
        <p style="font-weight: bold; margin-bottom: 0.5rem;">Graphic 1: The Core Mission</p>
        <img src="images/road_to_500k_minimal_fixed_1_1780685797290.png" alt="Road to 500k" style="max-width: 1000px; width: 100%; border-radius: 8px; margin-bottom: 2rem; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">

        <p style="font-weight: bold; margin-bottom: 0.5rem;">Graphic 2: Let's Build Momentum!</p>
        <img src="images/road_to_500k_minimal_fixed_2_1780685804208.png" alt="Let's Build Momentum to 500k!" style="max-width: 1000px; width: 100%; border-radius: 8px; margin-bottom: 2rem; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">

        <p style="font-weight: bold; margin-bottom: 0.5rem;">Website Tracker Previews</p>
        <img src="images/vdr_portal_preview.png" alt="VDR Portal Tracking Widget" style="max-width: 1000px; width: 100%; border-radius: 8px; margin-bottom: 1rem; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
        <img src="images/voter_tracker_preview.png" alt="Live Voter Registration Tracker" style="max-width: 1000px; width: 100%; border-radius: 8px; margin-bottom: 2rem; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">

        <hr style="margin: 2rem 0; border: none; border-top: 2px solid #e2e8f0;">

        <p style="font-size: 0.9rem; line-height: 1.6; color: #64748b;"><strong>ABOUT THE HIDALGO COUNTY DEMOCRATIC PARTY</strong><br>
        The Hidalgo County Democratic Party is dedicated to empowering the working families of South Texas, advocating for robust public education, accessible healthcare, and equal opportunities for all. Under the leadership of Chairman Richard Gonzalez, the Party is actively organizing to ensure every eligible voter has a voice in our democracy. Chairman Gonzalez is committed to building a sustainable, organized, and powerful political infrastructure in the Rio Grande Valley—leaving the Party stronger, larger, and more effective than ever before.</p>

        <div style="margin-top: 3rem; text-align: center;">
            <a href="press.html" style="background: var(--tx-navy); color: white; padding: 0.8rem 1.5rem; border-radius: 4px; text-decoration: none; font-weight: 600; font-size: 1.1rem; display: inline-block;">← Back to Press Releases</a>
        </div>
    </div>
    """
    
    with open('road_to_500k_press_release.html', 'w', encoding='utf-8') as f:
        f.write(header + content + footer)
    print("road_to_500k_press_release.html created.")
