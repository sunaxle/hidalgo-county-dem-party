const fs = require('fs');
const path = require('path');

const directoryPath = path.join(__dirname);

function findHtmlFiles(dir, fileList = []) {
  const files = fs.readdirSync(dir);

  files.forEach(file => {
    const filePath = path.join(dir, file);
    if (fs.statSync(filePath).isDirectory()) {
      if (file !== '.git' && file !== 'node_modules') {
        findHtmlFiles(filePath, fileList);
      }
    } else if (file.endsWith('.html')) {
      fileList.push(filePath);
    }
  });

  return fileList;
}

const htmlFiles = findHtmlFiles(directoryPath);

const newNavLinks = `    <div class="nav-links">
      <a href="index.html" class="nav-item">Home</a>
      
      <div class="nav-item dropdown">
        <span>About ▼</span>
        <div class="dropdown-content">
          <a href="about.html">About Us</a>
          <a href="bylaws.html">Bylaws</a>
          <a href="elected_officials.html">Elected Reps</a>
          <a href="precinct_chairs.html">Precinct Chairs</a>
        </div>
      </div>

      <div class="nav-item dropdown">
        <span>Action ▼</span>
        <div class="dropdown-content">
          <a href="volunteer.html">Volunteer</a>
          <a href="arena_training.html">The Arena</a>
          <a href="vote.html">Resources</a>
        </div>
      </div>

      <div class="nav-item dropdown">
        <span>Community ▼</span>
        <div class="dropdown-content">
          <a href="social_wall.html">Social Wall</a>
          <a href="county_websites.html">TX Dems</a>
          <a href="south_texas_region.html">South TX</a>
        </div>
      </div>

      <div class="nav-item dropdown">
        <span>Issues ▼</span>
        <div class="dropdown-content">
          <a href="issues_map.html">Issues Data Map</a>
          <a href="call_it_out.html">Call It Out Board</a>
          <a href="share_stories.html">Share Our Stories</a>
        </div>
      </div>

      <div class="nav-item dropdown">
        <span>Connect ▼</span>
        <div class="dropdown-content">
          <a href="community_inbox.html">Inbox</a>
          <a href="contact.html">Contact</a>
        </div>
      </div>
    </div>`;

htmlFiles.forEach(file => {
  let content = fs.readFileSync(file, 'utf8');
  
  // Use regex to replace the entire <div class="nav-links">...</div> block
  // We need to match from <div class="nav-links"> to its closing </div>
  // Because it can contain nested divs, a simple regex might be tricky,
  // but we know the structure has exactly 2 nested <div class="nav-item dropdown"> with their own </div>
  // Wait, let's just make it simple. The nav block starts at <div class="nav-links"> and ends before </nav>
  
  const navLinksStartRegex = /<div class="nav-links">([\s\S]*?)<\/nav>/;
  const match = content.match(navLinksStartRegex);
  
  if (match) {
    const replacement = newNavLinks + '\\n  </nav>';
    const newContent = content.replace(navLinksStartRegex, replacement);
    fs.writeFileSync(file, newContent, 'utf8');
    console.log(\`Updated \${file}\`);
  } else {
    console.log(\`Could not find nav component in \${file}\`);
  }
});

console.log('Nav replacement complete.');
