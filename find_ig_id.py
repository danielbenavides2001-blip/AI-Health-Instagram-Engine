import os
import requests
import sys
from dotenv import load_dotenv

# Ensure stdout uses UTF-8 if possible, or just avoid emojis
# sys.stdout.reconfigure(encoding='utf-8') # Only for Python 3.7+

load_dotenv()

token = os.getenv("FACEBOOK_PAGE_ACCESS_TOKEN")
page_id = os.getenv("FACEBOOK_PAGE_ID")

if not token or not page_id:
    print("[ERROR] FACEBOOK_PAGE_ACCESS_TOKEN or FACEBOOK_PAGE_ID not found in .env")
    exit(1)

print(f"--- Finding Instagram Account for Page: {page_id} ---")
url = f"https://graph.facebook.com/v20.0/{page_id}"
params = {
    "fields": "instagram_business_account,name",
    "access_token": token
}

try:
    response = requests.get(url, params=params)
    data = response.json()
    print("[SUCCESS] Page Response:")
    print(data)

    if "instagram_business_account" in data:
        ig_id = data["instagram_business_account"]["id"]
        print(f"\nFOUND! Linked Instagram ID: {ig_id}")
        
        # Suggest updating .env
        print(f"\nAdd this to your .env:\nIG_USER_ID={ig_id}")
    else:
        print("\n[ERROR] The page does not report any linked Instagram account with this token.")

except Exception as e:
    print(f"[ERROR] {e}")
