import asyncio
import logging
from google.antigravity import Agent, LocalAgentConfig
from google.antigravity.triggers import every, TriggerContext
import sys
import os

# Add scripts dir to path to import our scraper
sys.path.append(os.path.join(os.path.dirname(__file__), 'scripts'))
from voter_scraper_trigger import scrape_voter_count, update_js_file

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

async def daily_voter_scrape(ctx: TriggerContext):
    """Daily trigger to scrape voter count and update JS file."""
    logging.info("TRIGGER: Fired daily voter registration scrape.")
    
    count = scrape_voter_count()
    if count:
        success = update_js_file(count)
        if success:
            await ctx.send(f"Successfully scraped and appended today's voter count: {count}")
        else:
            await ctx.send(f"Scraped count ({count}), but failed to update JS file.")
    else:
        logging.error("Failed to extract count.")
        await ctx.send("Failed to extract the live voter count from the Hidalgo County Elections site.")

# Run once every 24 hours (86400 seconds)
# For testing purposes, we could lower this, but 24h is the intended production frequency
voter_trigger = every(86400, daily_voter_scrape)

async def main():
    logging.info("Starting Voter Tracker Daemon...")
    
    config = LocalAgentConfig(
        system_instructions="You are the Data Analyst Agent monitoring the Hidalgo County voter registration levels.",
        triggers=[voter_trigger]
    )

    # Initialize the agent with the trigger attached
    async with Agent(config) as agent:
        logging.info("Agent running in background. Waiting for triggers...")
        # Keep the daemon alive
        while True:
            await asyncio.sleep(3600)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Daemon shut down manually.")
