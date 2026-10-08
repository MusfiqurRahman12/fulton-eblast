"""
Optimize all production assets for email delivery.
Target: <1MB total weight, 1200px max width (2x retina for 600px email).
"""
from PIL import Image
import os

ASSETS_DIR = "assets"

def optimize(name, max_w=1200, quality=78, fmt=None):
    path = os.path.join(ASSETS_DIR, name)
    if not os.path.exists(path):
        print(f"  SKIP (missing): {name}")
        return
    img = Image.open(path)
    
    # Resize if wider than max_w
    if img.width > max_w:
        ratio = max_w / img.width
        new_h = int(img.height * ratio)
        img = img.resize((max_w, new_h), Image.LANCZOS)
    
    if fmt is None:
        fmt = "JPEG" if name.endswith(".jpg") else "PNG"
    
    if fmt == "JPEG":
        if img.mode == "RGBA":
            bg = Image.new("RGB", img.size, (65, 68, 70))
            bg.paste(img, mask=img.split()[3])
            img = bg
        elif img.mode != "RGB":
            img = img.convert("RGB")
        img.save(path, "JPEG", quality=quality, optimize=True)
    else:
        img.save(path, "PNG", optimize=True)
    
    sz = os.path.getsize(path)
    print(f"  {name}: {img.width}x{img.height} -> {sz//1024}KB")
    return sz

print("=== Optimizing for email delivery (1200px max, compressed) ===\n")

total = 0

# Hero composite (full top section)
total += optimize("hero-composite.jpg", 1200, 78) or 0

# Header banner
total += optimize("header-banner-2x.jpg", 1200, 78) or 0

# You're Invited banner  
total += optimize("youre-invited-2x.jpg", 1200, 78) or 0

# Top bar
total += optimize("top-bar-2x.png", 1200) or 0

# The Goat logo (keep at 484px or smaller — displayed at 242px)
total += optimize("goat-logo-2x.png", 484) or 0

# Interior photo
total += optimize("interior-photo-2x.jpg", 1060, 80) or 0

# Footer banner
total += optimize("footer-banner-2x.jpg", 1200, 75) or 0

# Logos (keep small)
total += optimize("alcova-logo-2x.png", 181) or 0
total += optimize("equal-housing-2x.png", 36) or 0
total += optimize("redeavor-logo-2x.png", 300) or 0

# Social icons (keep at 104px for 4x retina sharpness)
total += optimize("icon-fb-2x.png", 104) or 0
total += optimize("icon-ig-2x.png", 104) or 0

# Divider
total += optimize("divider-mauve-2x.png", 120) or 0

print(f"\n=== Total optimized size: {total//1024}KB ===")
