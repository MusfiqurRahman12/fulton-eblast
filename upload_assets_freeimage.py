"""
Upload all Fulton eblast assets to FreeImage.host (iili.io)
Direct high-speed HTTPS CDN endpoints matching Project ID 4498470078-001.
"""
import urllib.request
import urllib.parse
import json
import base64
import os
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = [
    "top-bar-2x.jpg",
    "header-banner-2x.jpg",
    "youre-invited-2x.jpg",
    "goat-logo-2x.png",
    "interior-photo-2x.jpg",
    "icon-fb-2x.png",
    "icon-ig-2x.png",
    "footer-banner-2x.jpg"
]

API_KEY = "6d207e02198a847aa98d0a2a901485a5"
UPLOAD_URL = "https://freeimage.host/api/1/upload"

hosted_map = {}

print("=== Uploading assets to FreeImage.host (iili.io) ===")
for filename in ASSETS:
    local_path = os.path.join(HERE, "assets", filename)
    if not os.path.exists(local_path):
        print(f"ERROR: {local_path} not found!")
        continue
    
    with open(local_path, "rb") as f:
        b64_data = base64.b64encode(f.read()).decode("utf-8")
    
    data = urllib.parse.urlencode({
        "key": API_KEY,
        "action": "upload",
        "source": b64_data,
        "format": "json"
    }).encode("utf-8")
    
    req = urllib.request.Request(
        UPLOAD_URL,
        data=data,
        headers={"User-Agent": "Mozilla/5.0"}
    )
    
    try:
        with urllib.request.urlopen(req) as resp:
            res = json.loads(resp.read().decode("utf-8"))
            if res.get("status_code") == 200:
                img_url = res["image"]["url"]
                hosted_map[f"assets/{filename}"] = img_url
                print(f"  OK: {filename} -> {img_url}")
            else:
                print(f"  FAILED: {filename} -> {res}")
    except Exception as e:
        print(f"  ERROR uploading {filename}: {e}")
    
    time.sleep(1) # respectful pause

# Save mapping
mapping_path = os.path.join(HERE, "hosted_assets.json")
with open(mapping_path, "w", encoding="utf-8") as f:
    json.dump(hosted_map, f, indent=2)
print(f"\nSaved asset mapping to {mapping_path}")

# Generate index-hosted.html
with open(os.path.join(HERE, "index.html"), "r", encoding="utf-8") as f:
    html_content = f.read()

hosted_html = html_content
for local_rel, remote_url in hosted_map.items():
    hosted_html = hosted_html.replace(f'"{local_rel}"', f'"{remote_url}"')
    hosted_html = hosted_html.replace(f"'{local_rel}'", f"'{remote_url}'")

hosted_html_path = os.path.join(HERE, "index-hosted.html")
with open(hosted_html_path, "w", encoding="utf-8") as f:
    f.write(hosted_html)
print(f"Generated {hosted_html_path} ({len(hosted_html)} bytes)")
