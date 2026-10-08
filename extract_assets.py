"""
Extract and slice all assets from the Fulton eblast PDF.
All assets saved locally — no remote upload.
Uses PIL for cropping from rendered pixmap.
"""
import pymupdf
import os
from PIL import Image
import io

PDF_PATH = "4559216753 - Fulton - Youre Invited Step Inside Fulton Eblast_v3.pdf"
ASSETS_DIR = "assets"
os.makedirs(ASSETS_DIR, exist_ok=True)

doc = pymupdf.open(PDF_PATH)
page = doc[0]

# Render full page at 2x retina (300 DPI)
DPI = 300
scale = DPI / 72.0
pix_full = page.get_pixmap(dpi=DPI)

# Convert pixmap to PIL Image for easy cropping
img_data = pix_full.tobytes("png")
full_img = Image.open(io.BytesIO(img_data))
print(f"Full page rendered: {full_img.width}x{full_img.height}")

def crop_and_save(name, top_pt, bottom_pt, left_pt=0, right_pt=600, fmt="PNG"):
    """Crop a region (coordinates in PDF points) and save."""
    left = int(left_pt * scale)
    top = int(top_pt * scale)
    right = int(right_pt * scale)
    bottom = int(bottom_pt * scale)
    
    # Clamp to image bounds
    right = min(right, full_img.width)
    bottom = min(bottom, full_img.height)
    
    cropped = full_img.crop((left, top, right, bottom))
    path = os.path.join(ASSETS_DIR, name)
    
    if fmt == "JPEG":
        # Convert RGBA to RGB for JPEG
        if cropped.mode == "RGBA":
            bg = Image.new("RGB", cropped.size, (255, 255, 255))
            bg.paste(cropped, mask=cropped.split()[3])
            cropped = bg
        cropped.save(path, "JPEG", quality=92, optimize=True)
    else:
        cropped.save(path, "PNG", optimize=True)
    
    print(f"  Saved: {path} ({cropped.width}x{cropped.height})")
    return path

print("=== Slicing sections from rendered page ===\n")

# 1. Top pricing bar (y: 0 to ~38)
crop_and_save("top-bar.png", 0, 38)

# 2. Header banner with Fulton logo + ivy/stone texture (y: ~35 to ~230)
crop_and_save("header-banner.jpg", 35, 230, fmt="JPEG")

# 3. "You're Invited" mauve banner section (y: ~228 to ~345)
crop_and_save("youre-invited-banner.png", 228, 345)

# 4. Full hero composite (top bar + header + mauve banner) for single-image approach
crop_and_save("hero-full-composite.jpg", 0, 345, fmt="JPEG")

# 5. Body text section - reference only (will be live HTML)
crop_and_save("body-text-reference.png", 345, 790)

# 6. The Goat logo (full region)
crop_and_save("the-goat-logo.png", 790, 915)

# 7. The Goat logo — tighter crop centered
crop_and_save("goat-logo-tight.png", 795, 912, 170, 430)

# 8. Event details: address, date/time
crop_and_save("event-details-reference.png", 930, 1035)

# 9. RSVP button + microcopy area
crop_and_save("rsvp-section-reference.png", 1038, 1145)

# 10. Interior residence photo (main showcase image)
crop_and_save("interior-photo.jpg", 1175, 1510, fmt="JPEG")

# 11. Reservation text + Schedule CTA
crop_and_save("schedule-section-reference.png", 1555, 1710)

# 12. Divider line
crop_and_save("divider-reference.png", 1730, 1770)

# 13. Explore / website CTA section
crop_and_save("explore-section-reference.png", 1770, 1870)

# 14. Social icons area
crop_and_save("social-icons-reference.png", 1890, 1950)

# 15. Address line
crop_and_save("address-reference.png", 1950, 1990)

# 16. Footer banner (stone/ivy + logos + legal)
crop_and_save("footer-banner.jpg", 2020, 2216, fmt="JPEG")

# 17. Footer logos - Alcova Capital + redeavor
crop_and_save("footer-logo-alcova.png", 2050, 2100, 45, 200)
crop_and_save("footer-logo-redeavor.png", 2050, 2100, 400, 570)

# 18. Equal Housing logo
crop_and_save("equal-housing-icon.png", 2112, 2140, 18, 48)

# 19. Facebook icon
crop_and_save("icon-facebook.png", 1897, 1937, 257, 297)

# 20. Instagram icon
crop_and_save("icon-instagram.png", 1897, 1937, 302, 342)

# === Extract embedded images directly from PDF (highest quality source) ===
print("\n=== Extracting embedded images from PDF ===\n")
images = page.get_images()
for i, img in enumerate(images):
    xref = img[0]
    base_image = doc.extract_image(xref)
    image_bytes = base_image["image"]
    ext = base_image["ext"]
    w = base_image["width"]
    h = base_image["height"]
    fname = f"embedded_{i}_xref{xref}_{w}x{h}.{ext}"
    fpath = os.path.join(ASSETS_DIR, fname)
    with open(fpath, "wb") as f:
        f.write(image_bytes)
    print(f"  Saved: {fpath} ({w}x{h}, {ext})")

print(f"\n=== Done! Total files in {ASSETS_DIR}/: {len(os.listdir(ASSETS_DIR))} ===")
doc.close()
