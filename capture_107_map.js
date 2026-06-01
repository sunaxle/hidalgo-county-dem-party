const puppeteer = require('puppeteer');
const path = require('path');

(async () => {
  try {
    const browser = await puppeteer.launch({
      args: ['--allow-file-access-from-files', '--disable-web-security', '--window-size=1200,800'],
      defaultViewport: null
    });
    const page = await browser.newPage();
    await page.setViewport({ width: 1200, height: 800 });
    
    // Use precinct_chairs.html as it has the map built-in
    const filePath = `file://${path.resolve('precinct_chairs.html')}`;
    console.log('Navigating to', filePath);
    await page.goto(filePath, { waitUntil: 'networkidle0' });
    
    console.log('Unlocking directory...');
    await page.type('#chair-password', 'ddddddd');
    await page.click('#btn-unlock');
    
    await new Promise(r => setTimeout(r, 1000));
    
    console.log('Searching for Precinct 107 to center map...');
    await page.type('#searchInput', '107');
    
    // Wait for map to pan, zoom and render the polygons
    await new Promise(r => setTimeout(r, 3000));
    
    const outputPath = path.resolve('images/precinct_107_map.png');
    console.log(`Taking screenshot of the map...`);
    
    // Select the map element to just capture the map instead of the whole page
    const mapElement = await page.$('#map');
    if (mapElement) {
        await mapElement.screenshot({ path: outputPath });
        console.log(`Saved screenshot to ${outputPath}`);
    } else {
        console.log("Could not find #map, taking full page screenshot");
        await page.screenshot({ path: outputPath, fullPage: true });
    }
    
    await browser.close();
    console.log('Done!');
  } catch(e) {
    console.error('Error:', e);
    process.exit(1);
  }
})();
