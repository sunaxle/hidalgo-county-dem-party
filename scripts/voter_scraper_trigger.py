import requests
from bs4 import BeautifulSoup
import re
import datetime
import os
import logging

logging.basicConfig(level=logging.INFO)

URL = "https://www.hidalgocounty.us/105/Elections-Department"
DATA_FILE = os.path.join(os.path.dirname(__file__), '..', 'js', 'voter_reg_data.js')

def scrape_voter_count():
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    try:
        response = requests.get(URL, headers=headers, timeout=15)
        if response.status_code != 200:
            logging.error(f"Failed to fetch page, status code: {response.status_code}")
            return None, None
        
        soup = BeautifulSoup(response.text, 'html.parser')
        page_text = soup.get_text(separator=' ')
        page_text = re.sub(r'\s+', ' ', page_text).strip()
        
        match = re.search(
            r"Registered Voters as of\s+([A-Za-z]+\s+\d{1,2},\s+\d{4})\s+Total\s+([\d,]+)", 
            page_text, 
            re.IGNORECASE
        )
        if match:
            date_str = match.group(1).strip()
            count_str = match.group(2).replace(',', '').strip()
            
            try:
                parsed_date = datetime.datetime.strptime(date_str, "%B %d, %Y").date()
                parsed_date_iso = parsed_date.strftime("%Y-%m-%d")
                return parsed_date_iso, int(count_str)
            except ValueError:
                logging.error(f"Failed to parse date string: {date_str}")
                return None, None
        else:
            logging.error("Could not find the 'Registered Voters as of' string on the page.")
            return None, None
            
    except Exception as e:
        logging.error(f"Error fetching/parsing page: {e}")
        return None, None

def update_js_file(voter_count, date_str=None):
    if not os.path.exists(DATA_FILE):
        logging.error(f"Data file not found at {DATA_FILE}")
        return False

    with open(DATA_FILE, 'r') as f:
        content = f.read()

    if date_str is None:
        date_str = datetime.date.today().strftime("%Y-%m-%d")
    
    # Chronological validation: Ensure we don't insert duplicate or older date entry
    existing_dates = re.findall(r'date:\s*"([^"]+)"', content)
    if existing_dates:
        last_date = existing_dates[-1]
        if date_str <= last_date:
            logging.info(f"Parsed date {date_str} is not newer than the latest entry {last_date} in the dataset. Skipping update.")
            return True

    match = re.search(r'(const voterRegistrationData = \[.*?)(];)', content, re.DOTALL)
    if not match:
        logging.error("Could not find voterRegistrationData array in js file.")
        return False
        
    array_content = match.group(1)
    new_entry = f'  {{ date: "{date_str}", count: {voter_count} }},\n'
    
    new_array_block = array_content + new_entry + "];"
    new_content = content.replace(match.group(0), new_array_block)

    with open(DATA_FILE, 'w') as f:
        f.write(new_content)
        
    logging.info(f"Successfully appended {date_str}: {voter_count} to {DATA_FILE}")
    return True

if __name__ == "__main__":
    logging.info("Starting manual scrape run...")
    date_str, count = scrape_voter_count()
    if count:
        logging.info(f"Scraped count: {count} as of {date_str}")
        update_js_file(count, date_str)
    else:
        logging.error("Scrape failed.")
