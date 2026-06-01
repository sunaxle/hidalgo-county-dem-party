const puppeteer = require('puppeteer');
const path = require('path');
const fs = require('fs');

(async () => {
  try {
    const browser = await puppeteer.launch({
      args: ['--allow-file-access-from-files', '--disable-web-security', '--window-size=1470,1200'],
      defaultViewport: null
    });
    const page = await browser.newPage();
    await page.setViewport({ width: 1470, height: 1200 });
    
    const filePath = `file://${path.resolve('precinct_chairs.html')}`;
    console.log('Navigating to', filePath);
    await page.goto(filePath, { waitUntil: 'networkidle0' });
    
    console.log('Unlocking directory...');
    await page.type('#chair-password', 'ddddddd');
    await page.click('#btn-unlock');
    
    await new Promise(r => setTimeout(r, 500));
    
    // Scrape first 5 occupied precincts
    const precinctsToCapture = await page.evaluate(() => {
      const rows = Array.from(document.querySelectorAll('.directory-row'));
      const pctSet = new Set();
      for (const row of rows) {
        if (row.dataset.precinct && !isNaN(parseInt(row.dataset.precinct))) {
          pctSet.add(row.dataset.precinct);
        }
        if (pctSet.size >= 5) break;
      }
      return Array.from(pctSet);
    });
    
    console.log('Capturing screenshots for precincts:', precinctsToCapture);
    
    const outputDir = '/Users/dr3/.gemini/antigravity/brain/231c903d-42ca-4076-90f2-1c2cc6b5e1c4/artifacts';
    if (!fs.existsSync(outputDir)) {
        fs.mkdirSync(outputDir, { recursive: true });
    }

    for (const pct of precinctsToCapture) {
      console.log(`Processing precinct ${pct}...`);
      
      // Clear input and type new precinct
      await page.evaluate(() => {
        const input = document.getElementById('searchInput');
        input.value = '';
        input.dispatchEvent(new Event('input', { bubbles: true }));
      });
      await new Promise(r => setTimeout(r, 200));
      
      await page.type('#searchInput', pct);
      // Wait for map zoom and render
      await new Promise(r => setTimeout(r, 2000));
      
      const outputPath = path.join(outputDir, `precinct_${pct}_highlight.png`);
      await page.screenshot({ path: outputPath, fullPage: true });
      console.log(`Saved screenshot to ${outputPath}`);
    }
    
    await browser.close();
    console.log('Done!');
  } catch(e) {
    console.error('Error:', e);
    process.exit(1);
  }
})();
