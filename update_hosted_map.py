import os
import json

HERE = os.path.dirname(os.path.abspath(__file__))

# Load hosted urls
with open(os.path.join(HERE, "hosted_assets.json"), "r") as f:
    base_hosted = json.load(f)

with open(os.path.join(HERE, "catbox_sliced_urls.json"), "r") as f:
    sliced_hosted = json.load(f)

# Combine all hosted assets
all_hosted = {**base_hosted}
for k, v in sliced_hosted.items():
    all_hosted[f"assets/{k}"] = v

with open(os.path.join(HERE, "hosted_assets.json"), "w") as f:
    json.dump(all_hosted, f, indent=2)

print("Updated hosted_assets.json with all 17 assets!")
