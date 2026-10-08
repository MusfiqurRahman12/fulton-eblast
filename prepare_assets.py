"""
Prepare optimized production assets for the Fulton eblast.
Resizes to email-standard widths (1200px = 2x retina for 600px display)
and compresses for fast loading.
"""
import pymupdf
from PIL import Image
import io
import os

PDF_PATH = "4559216753 - Fulton - Youre Invited Step Inside Fulton Eblast_v3.pdf"
ASSETS_DIR = "assets"

doc = pymupdf.open(PDF_PATH)
page = doc[0]

# Render at 2x retina (300 DPI = 1200px wide for a 600pt PDF)
DPI = 300
scale = DPI / 72.0
pix_full = page.get_pixmap(dpi=DPI)
img_data = pix_full.tobytes("png")
full_img = Image.open(io.BytesIO(img_data))

def crop_save(name, top_pt, bot_pt, l=0, r=600, fmt="PNG", quality=88):
    box = (int(l*scale), int(top_pt*scale), min(int(r*scale), full_img.width), min(int(bot_pt*scale), full_img.height))
    cropped = full_img.crop(box)
    path = os.path.join(ASSETS_DIR, name)
    if fmt == "JPEG":
        if cropped.mode == "RGBA":
            bg = Image.new("RGB", cropped.size, (65, 68, 70))
            bg.paste(cropped, mask=cropped.split()[3])
            cropped = bg
        cropped.save(path, "JPEG", quality=quality, optimize=True)
    else:
        cropped.save(path, "PNG", optimize=True)
    fsize = os.path.getsize(path)
    print(f"  {name}: {cropped.width}x{cropped.height} ({fsize//1024}KB)")

print("=== Building production assets ===\n")

# --- Hero composite: top-bar + header + youre-invited (single image, reduces HTTP requests) ---
crop_save("hero-composite.jpg", 0, 345, fmt="JPEG", quality=90)

# --- Header banner only (without top-bar and youre-invited) for flexibility ---
crop_save("header-banner-2x.jpg", 35, 228, fmt="JPEG", quality=90)

# --- You're Invited banner ---
crop_save("youre-invited-2x.jpg", 228, 345, fmt="JPEG", quality=90)

# --- Top pricing bar ---
crop_save("top-bar-2x.png", 0, 38)

# --- The Goat logo (transparent PNG extracted from PDF is better) ---
# The embedded xref192 is already a perfect transparent PNG
# Just copy and resize it
goat_src = Image.open(os.path.join(ASSETS_DIR, "embedded_7_xref192_1500x677.png"))
# Resize to 484px wide (242px display @ 2x) to match the PDF layout
goat_resized = goat_src.resize((484, int(484 * goat_src.height / goat_src.width)), Image.LANCZOS)
goat_resized.save(os.path.join(ASSETS_DIR, "goat-logo-2x.png"), "PNG", optimize=True)
print(f"  goat-logo-2x.png: {goat_resized.width}x{goat_resized.height} ({os.path.getsize(os.path.join(ASSETS_DIR, 'goat-logo-2x.png'))//1024}KB)")

# --- Interior photo ---
crop_save("interior-photo-2x.jpg", 1178, 1507, l=35, r=564, fmt="JPEG", quality=90)

# --- Footer banner ---
crop_save("footer-banner-2x.jpg", 2022, 2216, fmt="JPEG", quality=90)

# --- Alcova Capital logo (already extracted as transparent PNG) ---
alcova_src = Image.open(os.path.join(ASSETS_DIR, "embedded_4_xref186_181x74.png"))
alcova_2x = alcova_src.resize((181, 74), Image.LANCZOS)
alcova_2x.save(os.path.join(ASSETS_DIR, "alcova-logo-2x.png"), "PNG", optimize=True)
print(f"  alcova-logo-2x.png: {alcova_2x.width}x{alcova_2x.height}")

# --- Equal Housing icon ---
eho_src = Image.open(os.path.join(ASSETS_DIR, "embedded_5_xref188_293x293.png"))
eho_2x = eho_src.resize((36, 36), Image.LANCZOS)
eho_2x.save(os.path.join(ASSETS_DIR, "equal-housing-2x.png"), "PNG", optimize=True)
print(f"  equal-housing-2x.png: {eho_2x.width}x{eho_2x.height}")

# --- Social icons: Extracted from PDF vector paths (see generate_social_icons.py) ---
# Kept intact as transparent 4x retina PNGs
print("  icon-fb-2x.png, icon-ig-2x.png (vector transparent PNGs preserved)")

# --- Redeavor logo: Slice from the footer area ---
crop_save("redeavor-logo-2x.png", 2055, 2095, l=405, r=565)

# --- Divider line (small mauve line used between sections) ---
crop_save("divider-mauve-2x.png", 1738, 1746, l=270, r=330)

print("\n=== Production assets ready ===")

# Calculate total size
total = sum(os.path.getsize(os.path.join(ASSETS_DIR, f)) for f in os.listdir(ASSETS_DIR))
print(f"Total assets folder size: {total//1024}KB ({total//(1024*1024)}MB)")
doc.close()
