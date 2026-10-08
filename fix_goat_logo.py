"""
Fix The Goat logo — extract with proper transparency from PDF.
Also create a footer-logos-only image (just the sponsor logos without legal text).
"""
from PIL import Image
import os

ASSETS_DIR = "assets"

# The embedded PNG xref192 has mask data — it's indexed with transparency
# Let's check the raw file
goat = Image.open(os.path.join(ASSETS_DIR, "embedded_7_xref192_1500x677.png"))
print(f"Goat logo: mode={goat.mode}, size={goat.size}")
print(f"Has transparency: {goat.info.get('transparency', 'No')}")

# The image is in 'P' (palette) mode with a transparency index
# Convert to RGBA to get proper transparency
if goat.mode == 'P':
    goat_rgba = goat.convert("RGBA")
elif goat.mode == 'RGBA':
    goat_rgba = goat
else:
    goat_rgba = goat.convert("RGBA")

# Check if it's actually transparent or if the green is baked in
# Let's look at pixel (0,0) which should be background
pixel = goat_rgba.getpixel((0, 0))
print(f"Corner pixel (0,0): {pixel}")

# If the alpha is 0, it's transparent — good
# If it's opaque green, we need to remove it
if pixel[3] > 200:
    # Green is baked in — need to chroma-key remove it
    print("Green background is baked in — removing via chroma key...")
    import numpy as np
    data = np.array(goat_rgba)
    
    # The green background is approximately RGB(55, 95, 55) to (75, 125, 75)
    # More accurately from the image: dark olive/forest green
    r, g, b, a = data[:,:,0], data[:,:,1], data[:,:,2], data[:,:,3]
    
    # Create mask: where green channel dominates and it's a dark green
    green_mask = (g > r + 10) & (g > b + 10) & (r < 130) & (g < 170) & (b < 130)
    
    # Also catch the edges — softer approach
    data[green_mask, 3] = 0  # Set alpha to 0 for green pixels
    
    goat_clean = Image.fromarray(data)
else:
    print("Logo already has transparency!")
    goat_clean = goat_rgba

# Resize to 484px wide for email (displayed at 242px @ 2x)
w_target = 484
ratio = w_target / goat_clean.width
h_target = int(goat_clean.height * ratio)
goat_final = goat_clean.resize((w_target, h_target), Image.LANCZOS)
goat_final.save(os.path.join(ASSETS_DIR, "goat-logo-2x.png"), "PNG", optimize=True)
print(f"Saved goat-logo-2x.png: {goat_final.width}x{goat_final.height}")

# Verify by checking corner pixel again
verify = Image.open(os.path.join(ASSETS_DIR, "goat-logo-2x.png"))
print(f"Verified corner pixel: {verify.getpixel((0, 0))}")
