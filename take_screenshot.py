from playwright.sync_api import sync_playwright
import time
import os

def run():
    output_dir = "/Users/dr3/.gemini/antigravity/brain/359fe4f5-4016-4919-84d7-61b2d254c8fb/"
    os.makedirs(output_dir, exist_ok=True)
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1470, "height": 1200})
        
        # Capture VDR Portal
        file_url = "file:///Users/dr3/Documents/Antigravity%20Designs/Politics/hidalgo-county-dem-party/vdr_portal.html"
        print(f"Navigating to {file_url}")
        
        try:
            page.goto(file_url, wait_until="networkidle", timeout=15000)
        except Exception as e:
            print("Finished navigating.")
            
        time.sleep(2)
        vdr_path = os.path.join(output_dir, "vdr_portal_preview.png")
        page.screenshot(path=vdr_path, full_page=True)
        print(f"Saved: {vdr_path}")

        # Capture Voter Registration Tracker
        file_url2 = "file:///Users/dr3/Documents/Antigravity%20Designs/Politics/hidalgo-county-dem-party/voter_registration_tracker.html"
        print(f"Navigating to {file_url2}")
        
        try:
            page.goto(file_url2, wait_until="networkidle", timeout=15000)
        except Exception as e:
            print("Finished navigating.")
            
        time.sleep(3) # Wait for Chart.js animation
        tracker_path = os.path.join(output_dir, "voter_tracker_preview.png")
        page.screenshot(path=tracker_path, full_page=True)
        print(f"Saved: {tracker_path}")
            
        browser.close()

if __name__ == "__main__":
    run()
