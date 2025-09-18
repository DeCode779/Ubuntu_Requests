"""
Ubuntu-Inspired Image Fetcher (Enhanced Version)
"I am because we are"

This script embodies Ubuntu values by connecting to the global web community,
respectfully fetching shared images, and organizing them for later sharing.

Challenge Features:
- Handles multiple URLs
- Adds precautions for unknown sources
- Prevents duplicate downloads
- Inspects HTTP headers before saving
"""

import os
import requests
from urllib.parse import urlparse

# Directory for saving images
SAVE_DIR = "Fetched_Images"
os.makedirs(SAVE_DIR, exist_ok=True)  # Sharing & Community principle

def fetch_image(url):
    """
    Fetch and save an image from the given URL.
    Includes error handling, duplicate prevention, and header checks.
    """
    try:
        # Fetch resource with streaming
        response = requests.get(url, stream=True, timeout=10)
        response.raise_for_status()  # Respect principle: handle HTTP errors

        # --- Precaution 1: Check content type ---
        content_type = response.headers.get("Content-Type", "")
        if not content_type.startswith("image/"):
            print(f"⚠ Skipped (Not an image): {url}")
            return

        # Extract filename from URL
        parsed_url = urlparse(url)
        filename = os.path.basename(parsed_url.path)

        # Fallback filename if missing
        if not filename:
            filename = "downloaded_image.jpg"

        save_path = os.path.join(SAVE_DIR, filename)

        # --- Precaution 2: Prevent duplicates ---
        if os.path.exists(save_path):
            print(f"ℹ Skipped duplicate: {filename}")
            return

        # --- Precaution 3: Check important headers ---
        content_length = response.headers.get("Content-Length")
        if content_length and int(content_length) > 10 * 1024 * 1024:  # 10MB limit
            print(f"⚠ Skipped (File too large): {url}")
            return

        # Save image in binary mode
        with open(save_path, "wb") as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)

        print(f"✅ Image saved successfully at {save_path}")

    except requests.exceptions.RequestException as e:
        print(f"⚠ Failed to fetch {url}: {e}")

# =========================
# Main Program
# =========================

print("Ubuntu-Inspired Image Fetcher")
print("Enter image URLs separated by spaces:")
urls = input("> ").split()

for url in urls:
    fetch_image(url)