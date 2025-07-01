
from transformers import pipeline
import os

print("Starting download of Hugging Face model 'facebook/bart-large-mnli'...")
print("This is a one-time download of about 1.6 GB. Please be patient.")
print("-" * 30)

try:
    pipeline(
        "zero-shot-classification",
        model="facebook/bart-large-mnli"
    )
    print("\n✅ Success! Model has been downloaded and cached on your Mac.")
    print("You can now restart the Docker container.")
except Exception as e:
    print(f"\n❌ Download failed: {e}")
    print("Please check your internet connection (disable any VPN if active) and run this script again.")