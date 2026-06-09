import os
import time

from playwright.sync_api import sync_playwright


def run():
    output_dir = "/Users/dr3/.gemini/antigravity/brain/231c903d-42ca-4076-90f2-1c2cc6b5e1c4/artifacts"
    os.makedirs(output_dir, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1470, "height": 1200})

        file_url = "file:///Users/dr3/Documents/Antigravity%20Designs/Politics/hidalgo-county-dem-party/precinct_chairs.html"
        print(f"Navigating to {file_url}")

        try:
            page.goto(file_url, wait_until="networkidle", timeout=15000)
        except Exception as e:
            print("Finished navigating (ignoring some idle timeouts).")

        print("Unlocking directory...")
        page.fill("#chair-password", "ddddddd")
        page.click("#btn-unlock")
        time.sleep(1)

        precincts = page.evaluate("""() => {
            const rows = Array.from(document.querySelectorAll('.directory-row'));
            const pctSet = new Set();
            for (const row of rows) {
                if (row.dataset.precinct && !isNaN(parseInt(row.dataset.precinct))) {
                    pctSet.add(row.dataset.precinct);
                }
                if (pctSet.size >= 5) break;
            }
            return Array.from(pctSet);
        }""")

        print(f"Precincts to capture: {precincts}")

        for pct in precincts:
            print(f"Processing precinct {pct}...")
            # Trigger input event so the JS table filter catches it
            page.evaluate(f"""() => {{
                const input = document.getElementById('searchInput');
                input.value = '{pct}';
                input.dispatchEvent(new Event('input', {{ bubbles: true }}));
            }}""")

            # Wait for map animation
            time.sleep(2)

            output_path = os.path.join(output_dir, f"precinct_{pct}_highlight.png")
            page.screenshot(path=output_path, full_page=True)
            print(f"Saved: {output_path}")

        browser.close()


if __name__ == "__main__":
    run()
