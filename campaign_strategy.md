[[Politics]]

# Campaign Strategy & Subagent Directives

> [!CAUTION]
> **CRITICAL GLOBAL DIRECTIVE**: Under NO circumstances are any campaign team members or orchestrators to commit or push any code, files, or changes to GitHub or any remote repository. All changes must remain strictly local on the file system until the user explicitly grants permission to push.

## High-Level Synthesized Summary

Based on the recent output logs (`optimizer_log.md`, `orchestrator.log`), the team has made significant progress across both codebase modernization and political ground-game automation:

1. **Codebase Hygiene & Modernization**:
   - Automated formatting and syntax upgrades were applied across all Python scripts (via Ruff), enforcing modern standards like f-strings and fixing import order/exception logic.
   - Security vulnerabilities (e.g., `target="_blank"`) were patched across all HTML files.
   - Frontend assets (CSS/JS) were standardized, and redundant HTML5 attributes were scrubbed.
   - Standardized social icons were embedded into global navbars.

2. **Voter Registration Countdown Pipeline**:
   - A live "Days Remaining" countdown banner (targeting the October 5, 2026 deadline for the 20,000-voter goal) has been successfully injected into the local homepage.
   - Automated scripts (`generate_countdown_graphic_live.py` and `weekly_precinct_email_generator.py`) are now deployed to generate dynamic daily graphics and draft weekly precinct chair emails.

3. **Sub-Agent Operational Focus**:
   - **Mobile UI**: Optimizing CSS grids, iPhone 15 safe areas, hamburger menus, and WCAG color contrast.
   - **Precinct Operations**: Reconciling voter databases, mapping ZIP codes, and plotting early voting transit penalty hot-spots.
   - **Volunteer/Event Sync**: Testing Google Sheets webhooks, validating volunteer multi-select data, and live-syncing event RSVPs (e.g., virtual trainings, candidate mixers).

---

## Directives for Next Phase

1. **Sustain Automated Code Hygiene**:
   - Maintain strict linting and formatting via Ruff and Prettier. Any future changes should pass these automated checks before deployment to keep the repository clean and optimized.

2. **Capitalize on the Countdown Infrastructure**:
   - Ensure the newly deployed weekly email generator is utilized to blast precinct chairs consistently. The urgency of the 121-day countdown must be reinforced weekly.
   - Track metrics on volunteer sign-ups originating from the live countdown banner to evaluate its effectiveness toward the 20,000-voter goal.

3. **Expand Precinct & Event Tools**:
   - With early voting transit hot-spots mapped, prioritize volunteer block-walking and phone-banking allocations to those critical districts.
   - Finalize the volunteer webhook payloads so that all intake data reliably streams into the master CRM without manual intervention.

4. **Mobile First & Accessibility**:
   - Continue to enforce WCAG AAA contrast and mobile-first design scaling across all candidate profile and event RSVP pages.
