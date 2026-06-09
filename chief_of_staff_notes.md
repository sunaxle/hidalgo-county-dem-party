[[Politics]]

# Chief of Staff Notes

## Blockages Identified
1. **Hardcoded Path Errors in Orchestrator:** The local deployment scripts (e.g., `update_local_homepage.py` and self-prompter loops) are targeting incorrect paths like `~/Documents/Antigravity Designs/hidalgo-county-dem-party/mobile_prototype`. They are missing the `Politics/` subdirectory, causing "Directory does not exist" warnings and failing to update the web files.
2. **Root Directory Write Failures:** The `$op` (Outbox path) variable in the bash deployment script evaluated to empty, causing the script to attempt `cp` commands and file creations directly to the root directory `/` (e.g., `/Message_For_Spark.md`, `/texas_voter_registration_hdp_countdown.png`). This resulted in "Read-only file system" errors.
3. **Execution Errors:** There are syntax or command errors in the orchestrator log (`/bin/sh: generate_countdown_graphic_live.py: command not found`, `/bin/sh: index.html: command not found`), indicating scripts are being executed incorrectly or lacking executable permissions.
4. **Dropzone Archive Failure:** The orchestrator failed to archive `instructions.json` in Google Drive with an `[Errno 2] No such file or directory` error.

## Priority Shifts & Delegations
- **Delegation 1 (DevOps / Infrastructure):** Fix the orchestrator and deployment scripts. Update all hardcoded paths to accurately reflect the workspace (`/Users/dr3/Documents/Antigravity Designs/Politics/hidalgo-county-dem-party`). Fix the bash variables to prevent root-directory fallback and resolve the Google Drive Dropzone file moving issue.
- **Delegation 2 (Backend / Architecture):** Begin the **Migrate to `src/` Layout** task from the Project Board. Restructure the Python application folder layout to use a top-level `src/` directory to ensure reliable packaging.
- **Delegation 3 (Frontend / QA):** Pick up the **Accessibility (WCAG 2.2 AA) Audit** task from the Project Board. Ensure the new elements (like the countdown banner) and the rest of the web assets meet minimum contrast and tap-target baselines.
