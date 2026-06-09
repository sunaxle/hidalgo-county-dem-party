import asyncio

from playwright.async_api import async_playwright


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        print("Navigating...")
        await page.goto(
            "https://results.enr.clarityelections.com/TX/Hidalgo/126201/web.345435/#/detail/3",
            wait_until="networkidle",
        )
        await page.wait_for_timeout(3000)
        text = await page.content()
        with open("clarity_page.html", "w") as f:
            f.write(text)
        print("Saved to clarity_page.html")
        await browser.close()


asyncio.run(main())
