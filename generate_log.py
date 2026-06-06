import re
from datetime import datetime, timedelta

with open('/tmp/hcdp_weekly_log.txt', 'r') as f:
    log_data = f.read()

commits = log_data.split('commit ')[1:]

# Group commits by 6-hour intervals starting from the most recent one
parsed_commits = []
for commit in commits:
    lines = commit.strip().split('\n')
    hash_id = lines[0].strip()
    author = ""
    date_str = ""
    message = []
    
    idx = 1
    while idx < len(lines):
        line = lines[idx]
        if line.startswith('Author:'):
            author = line.replace('Author:', '').strip()
        elif line.startswith('Date:'):
            date_str = line.replace('Date:', '').strip()
        elif line.startswith('    '):
            message.append(line.strip())
        elif line == "":
            pass
        else:
            break
        idx += 1
        
    if date_str:
        # Date format: 2026-06-03 22:28:39 -0500
        dt = datetime.strptime(date_str[:-6].strip(), "%Y-%m-%d %H:%M:%S")
        parsed_commits.append({
            'hash': hash_id,
            'author': author,
            'date': dt,
            'message': " ".join(message)
        })

parsed_commits.sort(key=lambda x: x['date'], reverse=True)

if not parsed_commits:
    print("No commits parsed.")
    exit(0)

# Generate markdown
md = "# HCDP Antigravity Master Log\n\n"
md += "*Automatically generated retrospective log of the past week's work.*\n\n"

current_interval_start = None
for c in parsed_commits:
    # 6 hour intervals
    dt = c['date']
    interval_start = dt.replace(hour=(dt.hour // 6) * 6, minute=0, second=0, microsecond=0)
    if current_interval_start != interval_start:
        current_interval_start = interval_start
        interval_end = interval_start + timedelta(hours=6)
        md += f"## {interval_start.strftime('%Y-%m-%d %I:%M %p')} - {interval_end.strftime('%I:%M %p')}\n\n"
        
    md += f"- **[{c['hash'][:7]}]** {c['message']}\n"

with open('/Users/dr3/Library/CloudStorage/GoogleDrive-romerodeab@gmail.com/My Drive/Antigravity_Work_Logs/HCDP_Master_Log.md', 'w') as f:
    f.write(md)

print("Master log generated.")
