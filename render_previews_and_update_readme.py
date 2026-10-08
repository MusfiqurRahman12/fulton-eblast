import os
import subprocess
import zipfile
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
DELIV_DIR = os.path.join(HERE, "Deliverable")
PREVIEWS_DIR = os.path.join(DELIV_DIR, "previews")
EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

preview_html_path = os.path.join(DELIV_DIR, "index-hosted.html")
url = "file:///" + os.path.abspath(preview_html_path).replace("\\", "/")

def render_and_crop(out_name, width, height):
    out_file = os.path.abspath(os.path.join(PREVIEWS_DIR, out_name))
    cmd = [
        EDGE,
        "--headless=new",
        "--disable-gpu",
        "--hide-scrollbars",
        f"--window-size={width},{height}",
        f"--screenshot={out_file}",
        url
    ]
    subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if os.path.exists(out_file):
        im = Image.open(out_file)
        bg = im.getpixel((0, im.height - 1))
        last_y = im.height - 1
        for y in range(im.height - 1, 0, -1):
            row = [im.getpixel((x, y)) for x in range(0, im.width, 10)]
            if any(pix != bg for pix in row):
                last_y = y
                break
        cropped = im.crop((0, 0, im.width, min(last_y + 20, im.height)))
        cropped.save(out_file, optimize=True)
        print(f"  {out_name} rendered & cropped: {cropped.size} ({os.path.getsize(out_file)//1024} KB)")

print("=== Rendering screenshots ===")
render_and_crop("preview-desktop.png", 800, 2300)
render_and_crop("preview-mobile.png", 500, 2400)

# Re-zip deliverable
zip_path = os.path.join(HERE, "Fulton-Residences-Project-4559216753-Deliverable.zip")
with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
    for root, dirs, files in os.walk(DELIV_DIR):
        for file in files:
            full_p = os.path.join(root, file)
            rel_p = os.path.relpath(full_p, HERE)
            z.write(full_p, rel_p)

print("Updated Deliverable ZIP:", os.path.getsize(zip_path)//1024, "KB")
