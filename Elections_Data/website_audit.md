# HCDP Website-Wide Strategic Data Audit

Based on an architectural review of the entire HCDP repository, there is a wealth of strategic data and analytic potential hidden in our existing forms and pages.

## 1. Demographic & Micro-Targeting Data (`volunteer_master_survey.html`)
The Master Survey is capturing highly granular data, including:
- **Occupation/Influence**: `is_teacher` allows us to instantly segment educators, who are high-value influencers for local school board races and GOTV efforts.
- **Demographics**: `ethnicity` tracking helps build culturally relevant messaging.
- **Availability & Preferences**: `best_time` and `preferred_contact` give us the matrix for scheduling phone banks when volunteers actually answer.
- **Cross-Pollination**: `other_campaigns` reveals which local candidates have the most volunteer overlap with the party, helping us identify "super-volunteers" and potential coalitions.

## 2. Real-Time Sentiment & Issue Tracking (`community_intake.html` & `share_stories.html`)
- **Voter Anger/Motivation**: The `share_stories.html` form includes an `angryToggleBtn` and `storyIssue` tracker. This serves as an *incident reporting system* that allows us to measure what issues are currently making voters angry (which correlates directly with turnout motivation).
- **Issue Heatmapping**: By combining `issue_type` and `precinct` from the community intake forms, we can build geographic heatmaps of what issues matter where (e.g., "Drainage issues in Precinct 103" vs "School funding in Precinct 14").

## 3. Viral Coefficient & Organizer Tracking (`join.html`)
- **Referral Tracking**: The `join.html` form includes a `referred_by` field. We can use this to calculate the viral coefficient of our organizers and identify top-performing community members who are bringing in the most new signups.

## 4. Precinct-Level Performance (`precinct_*.html`)
- The repository contains several precinct dashboards (`precinct_profiles.html`, `precinct_performance.html`, `precinct_completion.html`, `interactive_precincts.html`). 
- We can extract historical turnout targets, track which precinct chairs are actually moving the needle, and cross-reference our "P192 Non Voters" (from the CRM) against precincts with chair vacancies to prioritize recruitment.
