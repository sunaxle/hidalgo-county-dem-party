#!/bin/bash

echo "Initiating 16-Agent Swarm Visual Demo (Extended 5-Minute Run)..."
sleep 1

# Window 1: Analysis & Learning Wing (Top Left)
osascript -e 'tell application "Terminal"
    do script "clear; echo -e \"\\033[1;32m[NEWS MONITOR AGENT]\\033[0m\"; echo \"Scanning local news...\"; sleep 5; echo \"[ALERT] Precinct 107 youth turnout anomaly detected (+400%).\"; sleep 2; echo -e \"\\n\\033[1;34m[DATA ANALYST AGENT]\\033[0m\"; echo \"Ingesting HCDP_Precinct_Contacts.csv...\"; for i in {1..20}; do printf \"[=====>    ] Parsing chunk %d/20...\\n\" \"$i\"; sleep 3; done; echo \"Cross-reference complete: 1,200 unregistered youth identified.\"; sleep 2; echo -e \"\\n\\033[1;36m[VOTER PROTECTION AGENT]\\033[0m\"; echo \"Scanning social media for Precinct 107 polling issues...\"; sleep 4; echo \"[CLEAR] No voter suppression tactics detected.\"; sleep 2; echo -e \"\\n\\033[1;35m[KNOWLEDGE TRACKER AGENT]\\033[0m\"; echo \"Updating personal_learning_tracker.md with new youth turnout trends...\"; sleep 5; echo \"Publishing Analysis Wing payload to Message Bus...\""
    set bounds of front window to {0, 25, 800, 450}
end tell'

# Window 2: Communications & Outreach Wing (Top Right)
osascript -e 'tell application "Terminal"
    do script "clear; echo -e \"\\033[1;35m[PRESS DRAFTER AGENT]\\033[0m\"; echo \"Awaiting data payload...\"; sleep 70; echo \"Drafting press release...\"; for i in {1..10}; do echo \"Evaluating semantic resonance pattern $i/10...\"; sleep 4; done; echo \"Press Release generated.\"; sleep 2; echo -e \"\\n\\033[1;36m[SOCIAL DRAFTER AGENT]\\033[0m\"; echo \"Generating Twitter thread and IG Carousel...\"; sleep 5; echo -e \"\\n\\033[1;32m[RELATIONAL ORGANIZER AGENT]\\033[0m\"; echo \"Querying CRM for micro-influencers in Precinct 107...\"; for i in {1..15}; do echo \"Matching profile $i/50...\"; sleep 3; done; echo \"Drafted 50 personalized email blasts.\"; sleep 2; echo -e \"\\n\\033[1;33m[DONOR ANALYST AGENT]\\033[0m\"; echo \"Filtering past donor database for youth-aligned issues...\"; sleep 5; echo \"Drafted rapid-response fundraising email.\"; sleep 2; echo \"Writing Comms artifacts to disk...\""
    set bounds of front window to {800, 25, 1600, 450}
end tell'

# Window 3: Engineering, Design & Compliance Wing (Bottom Left)
osascript -e 'tell application "Terminal"
    do script "clear; echo -e \"\\033[1;33m[COMPLIANCE HUB AGENT]\\033[0m\"; echo \"Monitoring Swarm Output...\"; sleep 10; echo \"Running continuous TRAIGA / TAC 219 Legal Checks...\"; for i in {1..15}; do echo \"Auditing data packet $i...\"; sleep 3.5; done; echo \"[PASSED] Strategies compliant.\"; sleep 2; echo -e \"\\n\\033[1;34m[INTENT NAVIGATOR AGENT]\\033[0m\"; echo \"Mocking up Youth Voter Hub splash page layout...\"; sleep 5; echo -e \"\\n\\033[1;31m[WEB DEVELOPER AGENT]\\033[0m\"; echo \"Scaffolding youth_voter_hub.html...\"; for i in {1..10}; do echo \"Compiling CSS module $i/10...\"; sleep 3; done; echo -e \"\\n\\033[1;35m[DESIGN CRITIC AGENT]\\033[0m\"; echo \"Reviewing visual hierarchy & glassmorphism aesthetic... PASSED.\"; sleep 3; echo -e \"\\n\\033[1;36m[ACCESSIBILITY AUDITOR AGENT]\\033[0m\"; echo \"Scanning for WCAG 2.2 compliance... Fixed aria-hidden tags.\"; sleep 3; echo -e \"\\n\\033[1;32m[ARCHITECTURE REFACTORER AGENT]\\033[0m\"; echo \"Validating Python Pydantic settings for data pipeline... PASSED.\"; sleep 2; echo \"Engineering Wing processing complete.\""
    set bounds of front window to {0, 450, 800, 900}
end tell'

# Window 4: Orchestrator & Field Wing (Bottom Right)
osascript -e 'tell application "Terminal"
    do script "clear; echo -e \"\\033[1;37m[ORCHESTRATOR NODE]\\033[0m\"; echo \"Swarm Initiated.\"; sleep 2; echo \"Spawning 16 subagents...\"; sleep 3; echo \"16/16 agents reporting active.\"; for i in {1..20}; do echo \"[$(date +%T)] Orchestrator heartbeat: Swarm processing at optimal capacity ($i/20)...\"; sleep 10; done; echo -e \"\\n\\033[1;32m[FIELD DIRECTOR AGENT]\\033[0m\"; echo \"Intercepted youth surge data.\"; sleep 3; echo \"Updating weekend canvas turfs to target Precinct 107.\"; sleep 3; echo -e \"\\n\\033[1;34m[VOLUNTEER COORDINATOR AGENT]\\033[0m\"; echo \"Drafting urgent SMS blast to shift existing volunteers to Precinct 107...\"; sleep 4; echo \"SMS queue ready.\"; sleep 2; echo -e \"\\n\\033[1;37m[ORCHESTRATOR NODE]\\033[0m\"; echo \"All Wings artifact check: PASSED.\"; echo \"SWARM EXECUTION COMPLETE.\""
    set bounds of front window to {800, 450, 1600, 900}
end tell'

echo "Extended 5-minute Demo launched! All 16 agents featured. Windows arranged in a 2x2 grid."
