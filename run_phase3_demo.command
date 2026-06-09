#!/bin/bash
cd "/Users/dr3/Documents/Antigravity Designs/Politics/hidalgo-county-dem-party"
clear
echo "========================="
echo "  PHASE 3 INTEGRATIONS  "
echo "========================="
sleep 1
python3 src/scripts/integrations/sync_mobilize.py
sleep 2
python3 src/scripts/integrations/sync_actblue.py
sleep 2
python3 src/scripts/dispatch/auto_dispatch_turf.py
sleep 2
python3 src/scripts/voter_protection/ballot_cure_sms.py
echo ""
echo "Phase 3 Demo Complete. You can close this window."
