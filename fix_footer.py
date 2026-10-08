"""
Create a footer banner that only has the stone/ivy texture + logos (no legal text).
"""
from PIL import Image
import pymupdf
import io
import os

ASSETS_DIR = "assets"
PDF_PATH = "4559216753 - Fulton - Youre Invited Step Inside Fulton Eblast_v3.pdf"

doc = pymupdf.open(PDF_PATH)
page = doc[0]

DPI = 300
scale = DPI / 72.0
pix_full = page.get_pixmap(dpi=DPI)
img_data = pix_full.tobytes("png")
full_img = Image.open(io.BytesIO(img_data))

# Footer banner: stone/ivy + logos only (y: 2022 to ~2110)
# This excludes the legal text (y: 2112+)
left = 0
top = int(2022 * scale)
right = full_img.width
bottom = int(2110 * scale)

footer_logos = full_img.crop((left, top, right, bottom))

# Resize to 1200px wide
target_w = 1200
ratio = target_w / footer_logos.width
target_h = int(footer_logos.height * ratio)
footer_logos = footer_logos.resize((target_w, target_h), Image.LANCZOS)

# Convert to RGB for JPEG
if footer_logos.mode == "RGBA":
    bg = Image.new("RGB", footer_logos.size, (65, 68, 70))
    bg.paste(footer_logos, mask=footer_logos.split()[3])
    footer_logos = bg

footer_logos.save(os.path.join(ASSETS_DIR, "footer-logos-banner-2x.jpg"), "JPEG", quality=82, optimize=True)
sz = os.path.getsize(os.path.join(ASSETS_DIR, "footer-logos-banner-2x.jpg"))
print(f"Saved footer-logos-banner-2x.jpg: {footer_logos.width}x{footer_logos.height} ({sz//1024}KB)")

doc.close()
