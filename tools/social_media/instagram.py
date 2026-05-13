import os
import time
from pathlib import Path
from typing import Optional
import datetime

import requests
from google.cloud import storage

from tools.common.base_model import BaseModelTool
from tools.common.messenger import Messenger


class InstagramTool(BaseModelTool):
    """
    Tool for interacting with Instagram Graph API.
    Handles Reels uploads.
    Instagram Graph API requires video files to be accessible via a public URL.
    This tool uses Google Cloud Storage to temporarily host the video.
    """
    ig_user_id: str
    access_token: str
    gcp_project_id: str
    gcs_bucket_name: str
    api_version: str = "v19.0"

    @property
    def base_url(self) -> str:
        return f"https://graph.facebook.com/{self.api_version}"

    # ====================================================================================
    # 🔒 LOCKED CONFIGURATION (DO NOT MODIFY) 🔒
    # The `upload_reel` method below uses the Google Cloud Storage Signed URL architecture.
    # This specific configuration is the ONLY reliable method proven to bypass Meta's
    # random 400 Bad Request 'ProcessingFailedError' bugs on direct binary uploads.
    # Do NOT revert to `rupload` binary streaming. Do NOT change the parameters.
    # ====================================================================================
    def upload_reel(
        self,
        file_path: Path,
        description: str = "",
    ) -> str:
        """
        Uploads a video to an Instagram Professional Account as a Reel
        using Google Cloud Storage and a Signed URL (the most stable method).
        """
        if not file_path.exists():
            raise FileNotFoundError(f"Video file not found: {file_path}")

        Messenger.info(f"🚀 Starting Instagram Reel GCS upload flow: {file_path.name}")

        # 1. Upload to GCS and get Signed URL
        Messenger.info(f"   Uploading video to Google Cloud Storage (Bucket: {self.gcs_bucket_name})...")
        storage_client = storage.Client(project=self.gcp_project_id)
        bucket = storage_client.bucket(self.gcs_bucket_name)
        
        # Ensure a unique filename to avoid caching issues
        blob_name = f"reels/instagram_{int(time.time())}_{file_path.name}"
        blob = bucket.blob(blob_name)
        
        # Upload the file
        blob.upload_from_filename(str(file_path), content_type="video/mp4")
        
        # Generate a Signed URL valid for 2 hours
        try:
            signed_url = blob.generate_signed_url(
                version="v4",
                expiration=datetime.timedelta(hours=2),
                method="GET"
            )
        except Exception as e:
            Messenger.warning(f"   Could not sign URL: {str(e)}")
            Messenger.info("   Attempting fallback: Making blob public temporarily...")
            try:
                blob.make_public()
                signed_url = blob.public_url
                Messenger.info(f"   Fallback successful: {signed_url}")
            except Exception as e2:
                Messenger.error(f"   Fallback failed: {str(e2)}")
                raise RuntimeError("Failed to generate a public URL for Meta. Ensure Service Account has 'Storage Object Admin' permissions.") from e

        Messenger.info("   Video securely hosted. URL generated.")

        # 2. Tell Instagram to fetch the video
        Messenger.info("   Instructing Instagram servers to download the video...")
        params = {
            "media_type": "REELS",
            "video_url": signed_url,
            "caption": description,
            "share_to_feed": "true",
            "access_token": self.access_token
        }
        
        response = requests.post(f"{self.base_url}/{self.ig_user_id}/media", data=params)
        
        if response.status_code != 200:
            Messenger.error(f"Container creation failed: {response.status_code} - {response.text}")
            response.raise_for_status()
            
        data = response.json()
        container_id = data["id"]
        
        Messenger.info(f"   Container created: {container_id}. Waiting for Meta's servers to process it...")

        # 3. Wait for processing
        self._wait_for_processing(container_id)

        # 4. Publish
        Messenger.info("   Publishing Reel to feed...")
        publish_params = {
            "creation_id": container_id,
            "access_token": self.access_token
        }
        publish_response = requests.post(f"{self.base_url}/{self.ig_user_id}/media_publish", data=publish_params)
        
        if publish_response.status_code != 200:
            Messenger.error(f"Publish failed: {publish_response.text}")
            publish_response.raise_for_status()
            
        published_id = publish_response.json()["id"]
        Messenger.success(f"✅ Reel published successfully! IG Media ID: {published_id}")
            
        return published_id

    def _wait_for_processing(self, container_id: str):
        """
        Polls the container status until it is FINISHED.
        URL-based uploads can take longer (up to 2-3 minutes).
        """
        max_attempts = 20  # ~1.5 minutes max (5s * 20)
        attempts = 0
        
        while attempts < max_attempts:
            params = {
                "fields": "status_code,status",
                "access_token": self.access_token
            }
            response = requests.get(f"{self.base_url}/{container_id}", params=params)
            response.raise_for_status()
            
            data = response.json()
            status_code = data.get("status_code")
            
            if status_code == "FINISHED":
                return
            elif status_code == "ERROR":
                status_details = data.get("status", "No detailed status provided")
                raise RuntimeError(f"Instagram video processing failed. Container status: ERROR. Details: {status_details}")
                
            attempts += 1
            time.sleep(5)
            
        raise RuntimeError(f"Timeout waiting for Instagram to process video.")
