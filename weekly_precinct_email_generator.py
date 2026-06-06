import os
from datetime import datetime

def generate_email():
    deadline = datetime(2026, 10, 5)
    today = datetime.now()
    diff = deadline - today
    days_remaining = max(0, diff.days + 1)
    
    email_content = f'''Subject: [COUNTDOWN] {days_remaining} Days Left to Register Voters — Weekly Precinct Chair Update

Hi [Precinct Chair Name],

We are officially {days_remaining} days away from the critical October 5, 2026 voter registration deadline for the Texas General Election!

To hit our local target of registering at least 20,000 new voters across Hidalgo County, we need a massive, coordinated push in every single neighborhood. As a Precinct Chair, you are the leading voice of our ground game.

Here is your weekly checklist to organize your precinct this week:

1. RUN THE COUNTDOWN GRAPHIC
Share our live B&W countdown infographic on your neighborhood group chats, social walls, or email chains. Only {days_remaining} days remain!

2. DOWNLOAD YOUR PRECINCT LISTS
Request local voter lists and register new neighbors using your Precinct VAN Access. If you need account credentials, email us at info@hidalgocountydems.org.

3. VOLUNTEER FOR PHONE BANKS & BLOCK WALKS
Sign up and coordinate shift schedules using our Master Volunteer Shift Survey:
https://hidalgocountydems.org/volunteer_master_survey.html

4. UPCOMING TRAINING AND MEETINGS
- Precinct Chair 101 Training: Wed, June 10, 5:30 PM - 6:30 PM (https://mobilize.us/s/YQ8PQh)
- "What's a Precinct Chair?" Info Session: Wed, June 17, 5:30 PM - 6:30 PM (https://mobilize.us/s/yUo7VI)

Thank you for stepping up to represent your neighborhood. Every registration counts towards our 20,000-voter milestone!

Best,

Richard Gonzales
County Chair, Hidalgo County Democratic Party
'''
    out_p = 'weekly_email_draft.txt'
    with open(out_p, 'w', encoding='utf-8') as f:
         f.write(email_content)
    print(f'Successfully generated weekly email draft ({days_remaining} Days Remaining) saved at: {out_p}')

if __name__ == '__main__':
    generate_email()
