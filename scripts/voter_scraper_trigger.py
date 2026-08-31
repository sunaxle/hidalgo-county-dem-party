import urllib.request
import re
import datetime
import os
import html
import ssl
import logging
import subprocess

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

URL = "https://www.hidalgocounty.us/105/Elections-Department"
DATA_FILE = os.path.join(os.path.dirname(__file__), '..', 'js', 'voter_reg_data.js')

def scrape_voter_count():
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    # Handle SSL verification on systems without configured CA certificates
    ctx = ssl.create_default_context()
    try:
        req = urllib.request.Request(URL, headers=headers)
        with urllib.request.urlopen(req, context=ctx, timeout=15) as response:
            html_content = response.read().decode('utf-8', errors='ignore')
    except Exception:
        # Fallback to unverified SSL context if standard SSL verification fails
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        try:
            req = urllib.request.Request(URL, headers=headers)
            with urllib.request.urlopen(req, context=ctx, timeout=15) as response:
                html_content = response.read().decode('utf-8', errors='ignore')
        except Exception as e:
            logging.error(f"Error fetching page {URL}: {e}")
            return None, None

    # HTML decode and clean whitespace
    text = html.unescape(html_content)
    text = re.sub(r'<[^>]+>', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()

    # Match "Registered Voters as of <date> Total <count>"
    match = re.search(
        r"Registered\s+Voters\s+as\s+of\s+([A-Za-z]+\s+\d{1,2},\s+\d{4})\s+Total\s+([\d,]+)", 
        text, 
        re.IGNORECASE
    )
    if match:
        date_str = match.group(1).strip()
        count_str = match.group(2).replace(',', '').strip()
        
        try:
            parsed_date = datetime.datetime.strptime(date_str, "%B %d, %Y").date()
            parsed_date_iso = parsed_date.strftime("%Y-%m-%d")
            return parsed_date_iso, int(count_str)
        except ValueError as e:
            logging.error(f"Failed to parse date string '{date_str}': {e}")
            return None, None
    else:
        logging.error("Could not find 'Registered Voters as of' text on the page.")
        return None, None

def update_js_file(voter_count, date_str):
    data_file_path = os.path.abspath(DATA_FILE)
    if not os.path.exists(data_file_path):
        logging.error(f"Data file not found at {data_file_path}")
        return False

    with open(data_file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check if entry for date already exists or if we already have a newer or same date
    existing_dates = re.findall(r'date:\s*"([^"]+)"', content)
    if existing_dates:
        last_date = existing_dates[-1]
        if date_str <= last_date:
            logging.info(f"Entry for date {date_str} (latest: {last_date}) is already recorded or older. Skipping update.")
            return True

    match = re.search(r'(const voterRegistrationData = \[.*?)(];)', content, re.DOTALL)
    if not match:
        logging.error("Could not find voterRegistrationData array in js file.")
        return False
        
    array_content = match.group(1)
    new_entry = f'  {{ date: "{date_str}", count: {voter_count} }},\n'
    
    new_array_block = array_content + new_entry + "];"
    new_content = content.replace(match.group(0), new_array_block)

    with open(data_file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
        
    logging.info(f"Successfully added {{ date: \"{date_str}\", count: {voter_count} }} to {data_file_path}")
    commit_and_push_changes(date_str, voter_count)
    return True

def commit_and_push_changes(date_str, voter_count):
    try:
        repo_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        # Stage js/voter_reg_data.js
        subprocess.run(["git", "add", "js/voter_reg_data.js"], cwd=repo_dir, check=True)
        
        # Check if there are staged changes
        status = subprocess.run(["git", "status", "--porcelain"], cwd=repo_dir, capture_output=True, text=True)
        if "js/voter_reg_data.js" not in status.stdout:
            logging.info("No changes in js/voter_reg_data.js to commit.")
            return True
            
        commit_msg = f"Auto-update voter registration data: {date_str} ({voter_count:,} registered voters)"
        subprocess.run(["git", "commit", "-m", commit_msg], cwd=repo_dir, check=True)
        logging.info(f"Committed changes: {commit_msg}")
        
        subprocess.run(["git", "push"], cwd=repo_dir, check=True)
        logging.info("Successfully pushed updates to Git repo (triggering website deployment).")
        return True
    except Exception as e:
        logging.error(f"Error during git commit/push: {e}")
        return False

if __name__ == "__main__":
    logging.info("Running voter scraper trigger...")
    parsed_date_iso, count = scrape_voter_count()
    if count and parsed_date_iso:
        logging.info(f"Scraped count: {count} as of {parsed_date_iso}")
        success = update_js_file(count, parsed_date_iso)
        if success:
            print(f"SUCCESS: Updated js/voter_reg_data.js with {parsed_date_iso}: {count}")
        else:
            print(f"FAILURE: Could not update js/voter_reg_data.js")
    else:
        print("FAILURE: Could not scrape voter count")
