import asyncio
import os
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, args=['--disable-web-security'])
        page = await browser.new_page(viewport={'width': 1200, 'height': 800})
        
        file_path = f"file://{os.path.abspath('precinct_chairs.html')}"
        print(f"Navigating to {file_path}")
        await page.goto(file_path, wait_until='load')
        
        print("Unlocking directory...")
        await page.fill('#chair-password', 'ddddddd')
        await page.click('#btn-unlock')
        
        await page.wait_for_timeout(2000)
        
        print("Searching for Precinct 107...")
        await page.fill('#searchInput', '107')
        
        # Wait for map to pan and zoom
        await page.wait_for_timeout(4000)
        
        output_path = os.path.abspath('images/precinct_107_map.png')
        print("Taking screenshot of the map...")
        
        map_element = await page.query_selector('#map')
        if map_element:
            await map_element.screenshot(path=output_path)
            print(f"Saved screenshot to {output_path}")
        else:
            print("Could not find #map, taking full page screenshot")
            await page.screenshot(path=output_path, full_page=True)
            
        await browser.close()

asyncio.run(main())
