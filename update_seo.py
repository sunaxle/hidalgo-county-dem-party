import os
import glob
import re

default_desc = "Official Website of the Hidalgo County Democratic Party. Empowering South Texas residents to build communities that represent them. Vote, Volunteer, and Get Involved."
og_image = "https://hidalgocountydems.org/images/facebook_1656248751972_6946810765393131439.webp"

json_ld = """
<!-- Local Business / Political Party JSON-LD -->
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "PoliticalParty",
  "name": "Hidalgo County Democratic Party",
  "url": "https://hidalgocountydems.org",
  "logo": "https://hidalgocountydems.org/images/facebook_1656248751972_6946810765393131439.webp",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "814 Del Oro Ln",
    "addressLocality": "Pharr",
    "addressRegion": "TX",
    "postalCode": "78577",
    "addressCountry": "US"
  },
  "telephone": "+1-956-672-7274",
  "email": "info@hidalgocountydems.org"
}
</script>
"""

html_files = glob.glob('*.html')

for filepath in html_files:
    with open(filepath, 'r') as f:
        content = f.read()

    # Extract title to reuse in OG
    title_match = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE)
    title = title_match.group(1) if title_match else "Hidalgo County Democrats"

    # Add <title> if missing
    if not title_match:
        content = re.sub(r'<head>', f'<head>\n  <title>{title}</title>', content, flags=re.IGNORECASE)

    # Extract or add description
    desc_match = re.search(r'<meta\s+name="description"\s+content="([^"]*)"', content, re.IGNORECASE)
    desc = desc_match.group(1) if desc_match else default_desc

    if not desc_match:
        content = re.sub(r'<head>', f'<head>\n  <meta name="description" content="{desc}">', content, flags=re.IGNORECASE)

    # Add OG Tags if not present
    if 'property="og:title"' not in content:
        og_tags = f"""
  <!-- Open Graph Tags -->
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:image" content="{og_image}">
  <meta property="og:type" content="website">
"""
        content = re.sub(r'</head>', f'{og_tags}</head>', content, flags=re.IGNORECASE)

    # Add JSON-LD to index.html and contact.html
    if filepath in ['index.html', 'contact.html', 'about.html']:
        if 'application/ld+json' not in content:
            content = re.sub(r'</head>', f'{json_ld}</head>', content, flags=re.IGNORECASE)

    with open(filepath, 'w') as f:
        f.write(content)

print(f"Updated {len(html_files)} HTML files with SEO metadata.")
