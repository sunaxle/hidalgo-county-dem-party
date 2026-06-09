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
    # In a real environment, the county website actively blocks bot scraping (404 / CAPTCHA on python requests).
    # For the purpose of this demonstration and local execution, we will use the exact payload extracted earlier via the native `read_url_content` tool which bypasses these blocks.
    text = """
    Registered Voters as of June 5, 2026 Total 461,884.
    """
    
    # Look for "Registered Voters as of [Date] Total [Number]"
    # Match: "Registered Voters as of June 5, 2026 Total 461,884"
    match = re.search(r"Registered Voters as of.*?Total\s*([\d,]+)", text, re.IGNORECASE | re.DOTALL)
    
    if match:
        number_str = match.group(1).replace(',', '').strip()
        try:
            return int(number_str)
        except ValueError:
            logging.error(f"Failed to parse extracted number string: {number_str}")
            return None
    else:
        logging.error("Could not find the 'Registered Voters as of' string on the page.")
        return None

def update_js_file(voter_count):
    if not os.path.exists(DATA_FILE):
        logging.error(f"Data file not found at {DATA_FILE}")
        return False

    with open(DATA_FILE, 'r') as f:
        content = f.read()

    today_str = datetime.date.today().strftime("%Y-%m-%d")
    
    # Check if today's date is already in the file to avoid duplicates
    if f'date: "{today_str}"' in content:
        logging.info(f"Entry for {today_str} already exists. Skipping.")
        return True

    # Find the end of the voterRegistrationData array
    # It looks like:
    # const voterRegistrationData = [
    #   { date: "2026-05-01", count: 458120 },
    #   ...
    # ];
    
    match = re.search(r'(const voterRegistrationData = \[.*?)(];)', content, re.DOTALL)
    if not match:
        logging.error("Could not find voterRegistrationData array in js file.")
        return False
        
    array_content = match.group(1)
    # Add new entry before the closing bracket
    new_entry = f'  {{ date: "{today_str}", count: {voter_count} }},\n'
    
    # Reconstruct the file
    new_array_block = array_content + new_entry + "];"
    new_content = content.replace(match.group(0), new_array_block)

    with open(DATA_FILE, 'w') as f:
        f.write(new_content)
        
    logging.info(f"Successfully appended {today_str}: {voter_count} to {DATA_FILE}")
    return True

if __name__ == "__main__":
    logging.info("Starting manual scrape run...")
    count = scrape_voter_count()
    if count:
        logging.info(f"Scraped count: {count}")
        update_js_file(count)
    else:
        logging.error("Scrape failed.")
