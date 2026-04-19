import os
import time

def send_mac_text():
    print("🚀 MAC iMESSAGE / SMS TAKEOVER")
    print("--------------------------------")
    
    phone_number = input("Enter your own cell phone number to test (e.g., 9566387581): ").strip()
    message = input("Enter a test message: ").strip()
    
    if not phone_number or not message:
        print("Error: Missing number or message.")
        return
        
    print(f"\n⏳ Commanding Mac Messages App to send payload to {phone_number}...")
    
    # Applescript payload
    # Note: If the user doesn't have iMessage, Messages app will automatically fall back 
    # to SMS (green bubble) if Text Message Forwarding is enabled on their iPhone.
    applescript = f'''
    tell application "Messages"
        -- Use the default service (handles both iMessage and SMS automatically)
        set targetService to 1st service whose service type = iMessage
        set targetBuddy to buddy "{phone_number}" of targetService
        send "{message}" to targetBuddy
    end tell
    '''
    
    # Execute the AppleScript via osascript
    # We write it to a temporary file, run it, then delete it.
    with open("temp_script.scpt", "w") as f:
        f.write(applescript)
        
    result = os.system("osascript temp_script.scpt")
    os.remove("temp_script.scpt")
    
    if result == 0:
        print("✅ SUCCESS! The Mac Messages App has successfully fired the text.")
        print("Open your Messages app on your Mac—you should physically see the text in your sent history!")
    else:
        print("❌ ERROR: The AppleScript failed to execute. Ensure your Messages app is open and configured.")

if __name__ == "__main__":
    send_mac_text()
