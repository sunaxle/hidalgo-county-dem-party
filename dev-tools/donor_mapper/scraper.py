import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE_URL = "https://www.hidalgocounty.us"
ROOT_DIR_URL = f"{BASE_URL}/1717/Campaign-Finance-Reports"

def init_workspace():
    # Make sure we have a clean directory to store our downloads
    downloads_dir = "downloads"
    if not os.path.exists(downloads_dir):
        os.makedirs(downloads_dir)
        print(f"Created isolated workspace: {downloads_dir}/")
    return downloads_dir

def fetch_candidate_categories():
    print(f"🕸️ Spawning Python Spider on target: {ROOT_DIR_URL}")
    
    # We use a standard user-agent so CivicPlus/Cloudflare doesn't block the Python request
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36'
    }
    
    try:
        response = requests.get(ROOT_DIR_URL, headers=headers)
        response.raise_for_status()
    except Exception as e:
        print(f"❌ Failed to puncture target server: {e}")
        return {}

    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Look for the internal structural links
    # Typical Hidalgo County site links look like /1719/Commissioner
    categories = {}
    
    for link in soup.find_all('a'):
        href = link.get('href')
        text = link.get_text(strip=True)
        
        # We know the specific target categories start with 17XX or 18XX in their root nav menu
        valid_targets = [
            'County Court at Law Judge',
            'Commissioner',
            'Constable',
            'County Official',
            'Justice of the Peace',
            'Specific Purpose Committee'
        ]
        
        if href and text in valid_targets:
            absolute_url = urljoin(BASE_URL, href)
            # Prevent duplicates
            if text not in categories:
                categories[text] = absolute_url

    return categories

def dig_into_category(category_name, category_url):
    print(f"\\n🔍 Digging into {category_name} hub: {category_url}")
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36'
    }
    
    try:
        response = requests.get(category_url, headers=headers)
        response.raise_for_status()
    except Exception as e:
        print(f"   [!] Failed to breach category {category_name}: {e}")
        return {}

    soup = BeautifulSoup(response.text, 'html.parser')
    candidate_links = {}
    
    # We are looking for rows or links that look like candidate profiles
    for link in soup.find_all('a'):
        href = link.get('href')
        text = link.get_text(strip=True)
        if href and len(text) > 4 and '/ArchiveCenter/ViewFile' not in href and '/DocumentCenter/' not in href:
             # Just trying to find candidate sub-pages or PDF links
             # If it's a PDF, we might catch it directly.
             if href.lower().endswith('.pdf') or 'DocumentCenter' in href:
                 candidate_links[text] = urljoin(BASE_URL, href)
             elif '/1' in href and not href.startswith('http'): # Internal routing link e.g. /1725/John-Doe
                 candidate_links[text] = urljoin(BASE_URL, href)

    return candidate_links

def download_candidate_reports(candidate_name, candidate_url):
    print(f"\\n⬇️ Extracting reports for {candidate_name}...")
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'
    }
    
    try:
        response = requests.get(candidate_url, headers=headers)
        response.raise_for_status()
    except Exception as e:
        print(f"   [!] Failed to load {candidate_name} profile: {e}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Create candidate folder
    candidate_folder = os.path.join('downloads', candidate_name.replace(' ', '_').replace(',', ''))
    if not os.path.exists(candidate_folder):
        os.makedirs(candidate_folder)
        
    pdf_count = 0
    # Search for PDF links
    for link in soup.find_all('a'):
        href = link.get('href')
        if href and ('DocumentCenter/View' in href or href.lower().endswith('.pdf')):
            pdf_url = urljoin(BASE_URL, href)
            pdf_name = link.get_text(strip=True).replace('/', '_').replace(' ', '_')
            if not pdf_name:
                pdf_name = f"Finance_Report_{pdf_count}.pdf"
            if not pdf_name.endswith('.pdf'):
                pdf_name += ".pdf"
                
            pdf_path = os.path.join(candidate_folder, pdf_name)
            
            # Download the PDF
            print(f"   📥 Downloading: {pdf_name}")
            try:
                # Use requests to get the PDF to handle headers/redirects
                r_pdf = requests.get(pdf_url, headers=headers, stream=True)
                if r_pdf.status_code == 200:
                    with open(pdf_path, 'wb') as f:
                        for chunk in r_pdf.iter_content(chunk_size=1024):
                            if chunk:
                                f.write(chunk)
                    pdf_count += 1
            except Exception as e:
                print(f"   [!] Failed to download {pdf_name}: {e}")
    
    if pdf_count > 0:
        print(f"   ✅ Successfully extracted {pdf_count} financial reports for {candidate_name}")
    else:
        print(f"   ⚠️ No PDF links detected on candidate profile.")

if __name__ == "__main__":
    init_workspace()
    category_links = fetch_candidate_categories()
    
    print("\\n✅ Successfully breached directory firewall. Located candidate hubs:")
    for name, url in category_links.items():
        print(f"📂 {name.upper()}: {url}")
        
    print("\\n🚀 INITIATING DEEP CRAWL & DOWNLOAD (Phase 1.C)...")
    cat_name = "County Court at Law Judge"
    cat_url = category_links[cat_name]
    
    print(f"\\n🎯 Targeting Category: {cat_name}")
    candidates = dig_into_category(cat_name, cat_url)
    
    # Just run on the first candidate to prove the concept without DDOSing their server
    first_candidate_name = list(candidates.keys())[2] # Target Gonzalez, Rodolfo Rudy
    first_candidate_url = candidates[first_candidate_name]
    
    print(f"\\n🎯 Targeting Candidate Zero: {first_candidate_name}")
    download_candidate_reports(first_candidate_name, first_candidate_url)
