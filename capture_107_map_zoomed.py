import asyncio
import os
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, args=['--disable-web-security'])
        page = await browser.new_page(viewport={'width': 1200, 'height': 800})
        
        file_path = f"file://{os.path.abspath('precinct_chairs.html')}"
        await page.goto(file_path, wait_until='load')
        
        await page.fill('#chair-password', 'ddddddd')
        await page.click('#btn-unlock')
        
        await page.wait_for_timeout(2000)
        
        await page.fill('#searchInput', '107')
        
        # Wait for map to pan and zoom initially
        await page.wait_for_timeout(4000)
        
        # Force the map to zoom in closer.
        # Since it's a Google Map, we can try evaluating a script if the map instance is global,
        # or we can double click the center of the map a few times.
        map_bounds = await page.locator('#map').bounding_box()
        if map_bounds:
            center_x = map_bounds['x'] + map_bounds['width'] / 2
            center_y = map_bounds['y'] + map_bounds['height'] / 2
            # double click to zoom in
            await page.mouse.click(center_x, center_y, click_count=2)
            await page.wait_for_timeout(1000)
            await page.mouse.click(center_x, center_y, click_count=2)
            await page.wait_for_timeout(2000)

        output_path = os.path.abspath('images/precinct_107_map_zoomed.png')
        map_element = await page.query_selector('#map')
        if map_element:
            await map_element.screenshot(path=output_path)
            print(f"Saved zoomed screenshot to {output_path}")
            
        await browser.close()

asyncio.run(main())
