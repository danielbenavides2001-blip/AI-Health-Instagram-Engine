import os
from google.cloud import storage
from dotenv import load_dotenv

load_dotenv()

project_id = os.getenv("GCP_PROJECT_ID")

if not project_id:
    print("[ERROR] GCP_PROJECT_ID not found in .env")
    exit(1)

print(f"--- Listing Buckets for Project: {project_id} ---")
try:
    storage_client = storage.Client(project=project_id)
    buckets = list(storage_client.list_buckets())
    
    if not buckets:
        print("[INFO] No buckets found in this project.")
    else:
        print("[SUCCESS] Buckets found:")
        for bucket in buckets:
            print(f"- {bucket.name}")

except Exception as e:
    print(f"[ERROR] {e}")
