import os
import shutil

# Find Google Drive path
d = next((p for p in [os.path.join(os.path.expanduser('~'), 'Library/CloudStorage', f, 'My Drive') for f in (os.listdir(os.path.join(os.path.expanduser('~'), 'Library/CloudStorage')) if os.path.exists(os.path.join(os.path.expanduser('~'), 'Library/CloudStorage')) else [])] + [os.path.join(os.path.expanduser('~'), 'Google Drive/My Drive')] if os.path.exists(p)), None)

if d:
    o = os.path.join(d, 'Work/Agent Dropzone/Agent Outbox')
    
    # Create the requested directory structure in the Outbox
    os.makedirs(os.path.join(o, 'js'), exist_ok=True)
    os.makedirs(os.path.join(o, 'images'), exist_ok=True)
    os.makedirs(os.path.join(o, 'data'), exist_ok=True)
    
    # Project root path
    p = os.path.join(os.path.expanduser('~'), 'Documents/Antigravity Designs/Politics/hidalgo-county-dem-party')
    
    # Execute the file copies
    try:
        shutil.copy(os.path.join(p, 'ultimate_van_email.html'), os.path.join(o, 'ultimate_van_email.html'))
        shutil.copy(os.path.join(p, 'van_concierge.html'), os.path.join(o, 'van_concierge.html'))
        shutil.copy(os.path.join(p, 'van_auto_sender.js'), os.path.join(o, 'js/van_auto_sender.js'))
        shutil.copy(os.path.join(p, 'images/van_tutorial_v3.gif'), os.path.join(o, 'images/van_tutorial_v3.gif'))
        shutil.copy(os.path.join(p, 'data/precinct_chairs_without_van.csv'), os.path.join(o, 'data/precinct_chairs_without_van.csv'))
        print("All 5 files successfully packaged and synced to Agent Outbox.")
    except Exception as e:
        print(f"Error copying files: {e}")
else:
    print('Google Drive mount not found.')
