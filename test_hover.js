const puppeteer = require('puppeteer');
(async () => {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  
  page.on('console', msg => console.log('PAGE LOG:', msg.text()));
  page.on('pageerror', error => console.log('PAGE ERROR:', error.message));

  await page.goto('file:///Users/dr3/Documents/Antigravity Designs/Politics/hidalgo-county-dem-party/precinct_chairs.html', {waitUntil: 'networkidle0'});
  await page.setViewport({ width: 1200, height: 800 });
  await page.type('#searchInput', '99');
  
  await new Promise(resolve => setTimeout(resolve, 1000));
  
  await page.screenshot({path: 'before_hover.png'});
  
  await page.evaluate(() => {
    // Find layer for precinct 99
    let target;
    map.eachLayer(l => {
      if (l.options && l.options.isSearchedPrecinct) {
        target = l;
      }
    });
    if (target) {
        target.fire('mouseover');
    }
  });
  
  await new Promise(resolve => setTimeout(resolve, 500));
  await page.screenshot({path: 'during_hover.png'});
  
  await page.evaluate(() => {
    // Find layer for precinct 99
    let target;
    map.eachLayer(l => {
      if (l.options && l.options.isSearchedPrecinct) {
        target = l;
      }
    });
    if (target) {
        target.fire('mouseout');
    }
  });
  
  await new Promise(resolve => setTimeout(resolve, 500));
  await page.screenshot({path: 'after_hover.png'});
  
  await browser.close();
})();
