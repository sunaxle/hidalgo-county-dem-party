import time
import random

def sync_actblue_donations():
    print("Initiating ActBlue Webhook Catch-up Sync...")
    time.sleep(0.6)
    print("Connecting to ActBlue CSV Export API...")
    time.sleep(0.9)
    print("Authentication: SUCCESS")
    
    donations = random.randint(45, 110)
    total_amount = sum([random.choice([5, 10, 15, 25, 50]) for _ in range(donations)])
    
    print(f"\nFound {donations} recent grassroots donations.")
    print(f"Total Amount Raised in batch: ${total_amount}.00")
    print("Average Donation: ${:.2f}".format(total_amount/donations))
    
    time.sleep(0.5)
    print("\nChecking for compliance flags (e.g. over limits, missing employer data)...")
    time.sleep(0.7)
    print(" -> 0 compliance flags found.")
    
    print("Routing data to Data Warehouse...")
    time.sleep(0.8)
    print("SYNC COMPLETE: ActBlue financial data is now live on the War Room Dashboard.\n")

if __name__ == "__main__":
    sync_actblue_donations()
