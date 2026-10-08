import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(HERE, "hosted_assets.json"), "r", encoding="utf-8") as f:
    hosted_map = json.load(f)

with open(os.path.join(HERE, "index.html"), "r", encoding="utf-8") as f:
    html = f.read()

for local_rel, remote_url in hosted_map.items():
    html = html.replace(f'"{local_rel}"', f'"{remote_url}"')
    html = html.replace(f"'{local_rel}'", f"'{remote_url}'")

out_path = os.path.join(HERE, "index-hosted.html")
with open(out_path, "w", encoding="utf-8") as f:
    f.write(html)

print(f"Generated {out_path} ({len(html)} bytes)")
for k, v in hosted_map.items():
    print(f"  {k} -> {v} : {'FOUND' if v in html else 'MISSING'}")
