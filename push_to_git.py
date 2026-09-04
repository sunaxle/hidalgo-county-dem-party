import subprocess
import os

os.system("rm -f .git/index.lock")

# Add exact files
files = [
    "contact.html",
    "subscribe.html",
    "community_intake.html",
    "home.html",
    "index.html",
    "about.html",
    "press.html",
    "crm_admin.html",
    "precinct_chairs_admin.html",
    "js/admin_feed.js",
    "js/form_handler.js",
    "js/share_stories.js",
    "js/crm_admin.js",
    "robots.txt",
    "sitemap.xml",
    "firestore.rules",
    "firebase.json"
]
for f in files:
    subprocess.run(["git", "add", f], env=dict(os.environ, GIT_CONFIG_GLOBAL="/dev/null"))

subprocess.run(["git", "commit", "-m", "Fix portal data feed, form submissions, and Google SEO schema"], env=dict(os.environ, GIT_CONFIG_GLOBAL="/dev/null"))
res = subprocess.run(["git", "push", "origin", "main"], capture_output=True, text=True, env=dict(os.environ, GIT_CONFIG_GLOBAL="/dev/null"))
print("PUSH RESULT:")
print("STDOUT:", res.stdout)
print("STDERR:", res.stderr)
print("CODE:", res.returncode)
