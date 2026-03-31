import { prepare, layout } from '@chenglou/pretext';
import { load } from 'cheerio';
import * as glob from 'glob';
import * as fs from 'fs';
import * as path from 'path';

// Define parameters
const MOBILE_BUTTON_MAX_WIDTH = 260; // Narrow width constraint for a button
const FONT_SPEC = '600 16px Inter'; 

async function runLinter() {
    const repoDir = path.resolve(__dirname, '../../');
    const htmlFiles = glob.sync('*.html', { cwd: repoDir, absolute: true });
    
    let totalItems = 0;
    let overflowCount = 0;

    console.log(`\n🔍 Analyzing ${htmlFiles.length} HTML files with @chenglou/pretext...`);
    console.log(`Constraint: maxWidth = ${MOBILE_BUTTON_MAX_WIDTH}px, font = "${FONT_SPEC}"\n`);

    for (const file of htmlFiles) {
        const content = fs.readFileSync(file, 'utf8');
        const $ = load(content);
        
        // Select typical components 
        const buttons = $('[class*="btn"], a[class*="button"], button');
        const headings = $('h1, h2');
        if (buttons.length === 0 && headings.length === 0) continue;

        let fileIssues: any[] = [];

        // Check buttons
        buttons.each((i, el) => {
            const text = $(el).text().trim().replace(/\s+/g, ' ');
            if (!text || text.length < 3) return;
            totalItems++;

            try {
                const prepared = prepare(text, FONT_SPEC);
                const { height, lineCount } = layout(prepared, MOBILE_BUTTON_MAX_WIDTH, 20);
                if (lineCount > 1) {
                    fileIssues.push({ type: 'Button', text, lineCount });
                    overflowCount++;
                }
            } catch (e) {}
        });

        // Check headings
        headings.each((i, el) => {
            const text = $(el).text().trim().replace(/\s+/g, ' ');
            if (!text || text.length < 3) return;
            totalItems++;

            try {
                // Headings are typically larger, e.g. 32px
                const prepared = prepare(text, '800 32px Inter');
                const { height, lineCount } = layout(prepared, 280, 40); // 280px max width
                // If heading is more than 3 lines on mobile, it's taking up too much vertical space
                if (lineCount > 3) {
                    fileIssues.push({ type: 'Heading', text, lineCount });
                    overflowCount++;
                }
            } catch (e) {}
        });

        if (fileIssues.length > 0) {
            console.log(`❌ [${path.basename(file)}]`);
            fileIssues.forEach((issue: any) => {
                console.log(`   - [${issue.type}] "${issue.text}" -> breaks into ${issue.lineCount} lines on mobile!`);
            });
        }
    }

    console.log(`\n📊 Summary: Checked ${totalItems} UI components.`);
    if (overflowCount > 0) {
        console.log(`⚠️ Found ${overflowCount} instances where component strings wrap excessively on mobile screens.`);
    } else {
        console.log(`✅ All layout checks passed.`);
    }
}

runLinter();