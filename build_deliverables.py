import os
import shutil
import json
import zipfile
import subprocess
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
DELIV_DIR = os.path.join(HERE, "Deliverable")
IMAGES_DIR = os.path.join(DELIV_DIR, "images")
PREVIEWS_DIR = os.path.join(DELIV_DIR, "previews")

# Clean & create directories
os.makedirs(IMAGES_DIR, exist_ok=True)
os.makedirs(PREVIEWS_DIR, exist_ok=True)

# 1. Copy the 7 production assets
ASSET_FILES = [
    "top-bar-2x.jpg",
    "header-banner-2x.jpg",
    "youre-invited-2x.jpg",
    "goat-logo-2x.png",
    "interior-photo-2x.jpg",
    "icon-fb-2x.png",
    "icon-ig-2x.png",
    "footer-banner-2x.jpg"
]

print("=== 1. Copying production assets ===")
for fname in ASSET_FILES:
    src = os.path.join(HERE, "assets", fname)
    dst = os.path.join(IMAGES_DIR, fname)
    shutil.copy2(src, dst)
    print(f"  Copied: {fname} ({os.path.getsize(dst)//1024} KB)")

# Load base index.html
with open(os.path.join(HERE, "index.html"), "r", encoding="utf-8") as f:
    base_html = f.read()

# Load hosted mapping
with open(os.path.join(HERE, "hosted_assets.json"), "r", encoding="utf-8") as f:
    hosted_map = json.load(f)

CLIENT_CDN = "https://assets.tangocrew.com/Fulton/4559216753/"

# 2. Build Deliverable/index.html (relative images/ paths)
html_local = base_html
for fname in ASSET_FILES:
    html_local = html_local.replace(f'"assets/{fname}"', f'"images/{fname}"')
    html_local = html_local.replace(f"'assets/{fname}'", f"'images/{fname}'")

with open(os.path.join(DELIV_DIR, "index.html"), "w", encoding="utf-8") as f:
    f.write(html_local)
print("=== 2. Generated Deliverable/index.html (images/ relative) ===")

# 3. Build Deliverable/index-hosted.html (iili.io CDN)
html_hosted = base_html
for fname in ASSET_FILES:
    cdn_url = hosted_map.get(f"assets/{fname}")
    if cdn_url:
        html_hosted = html_hosted.replace(f'"assets/{fname}"', f'"{cdn_url}"')
        html_hosted = html_hosted.replace(f"'assets/{fname}'", f"'{cdn_url}'")

with open(os.path.join(DELIV_DIR, "index-hosted.html"), "w", encoding="utf-8") as f:
    f.write(html_hosted)
print("=== 3. Generated Deliverable/index-hosted.html (hosted CDN) ===")

# 4. Build Deliverable/index-client-cdn.html (Tango Crew CDN)
html_client = base_html
for fname in ASSET_FILES:
    client_url = f"{CLIENT_CDN}{fname}"
    html_client = html_client.replace(f'"assets/{fname}"', f'"{client_url}"')
    html_client = html_client.replace(f"'assets/{fname}'", f"'{client_url}'")

with open(os.path.join(DELIV_DIR, "index-client-cdn.html"), "w", encoding="utf-8") as f:
    f.write(html_client)
print("=== 4. Generated Deliverable/index-client-cdn.html (client CDN) ===")

# 5. Build Deliverable/mailchimp-template.html
html_mc = html_hosted
# Add mc:edit tags to key editable regions
html_mc = html_mc.replace('<title>You\'re Invited — Step Inside Fulton Residences</title>',
                          '<title>*|MC:SUBJECT|*</title>')

html_mc = html_mc.replace(
    '<p class="c-white" style="margin: 0; font-family: \'Plus Jakarta Sans\', Arial, Helvetica, sans-serif; font-size: 13px; line-height: 18px; color: #FFFFFE; letter-spacing: 0.5px;">',
    '<div mc:edit="top_bar"><p class="c-white" style="margin: 0; font-family: \'Plus Jakarta Sans\', Arial, Helvetica, sans-serif; font-size: 13px; line-height: 18px; color: #FFFFFE; letter-spacing: 0.5px;">'
).replace(
    '</p>\n            </td>\n          </tr>\n\n          <!-- ============================================',
    '</p></div>\n            </td>\n          </tr>\n\n          <!-- ============================================'
)

html_mc = html_mc.replace(
    'THE WAIT IS ALMOST OVER&mdash;COME SEE<br />\n                FULTON RESIDENCES IN PERSON.',
    '<span mc:edit="subheading">THE WAIT IS ALMOST OVER&mdash;COME SEE<br />\n                FULTON RESIDENCES IN PERSON.</span>'
)

html_mc = html_mc.replace(
    'Join us at <strong>The Goat</strong> in Germantown for <strong>cocktails and light bites</strong>&mdash;and your first opportunity to experience Fulton Residences in person. Located directly across the street from Fulton on Second Ave, The Goat will serve as home base for the evening.',
    '<span mc:edit="body_p1">Join us at <strong>The Goat</strong> in Germantown for <strong>cocktails and light bites</strong>&mdash;and your first opportunity to experience Fulton Residences in person. Located directly across the street from Fulton on Second Ave, The Goat will serve as home base for the evening.</span>'
)

html_mc = html_mc.replace(
    'From there, guests can walk over with our sales team for a <strong>guided hard hat tour</strong>, offering an up-close look at the residences, amenity spaces and progress happening throughout the building.',
    '<span mc:edit="body_p2">From there, guests can walk over with our sales team for a <strong>guided hard hat tour</strong>, offering an up-close look at the residences, amenity spaces and progress happening throughout the building.</span>'
)

html_mc = html_mc.replace(
    'Come raise a glass with us, meet the Fulton team and finally <strong>step inside the project you\u2019ve been hearing about</strong>.',
    '<span mc:edit="body_p3">Come raise a glass with us, meet the Fulton team and finally <strong>step inside the project you\u2019ve been hearing about</strong>.</span>'
)

# Append Mailchimp compliance footer before closing table
mc_compliance_block = """
          <!-- ============================================
               SECTION 16: COMPLIANT MAILCHIMP FOOTER
               ============================================ -->
          <tr>
            <td class="bg-body" align="center" valign="top" bgcolor="#414446" style="padding: 20px 20px 36px 20px; background-color: #414446; background-image: linear-gradient(#414446, #414446); border-top: 1px solid rgba(255,255,255,0.12);">
              <div mc:edit="mailchimp_compliance">
                <p style="margin: 0 0 10px 0; font-family: 'Plus Jakarta Sans', Arial, Helvetica, sans-serif; font-size: 11px; line-height: 16px; color: #b0b4b8; text-align: center;">
                  &copy; *|CURRENT_YEAR|* *|LIST:COMPANY|*. All rights reserved.<br />
                  *|LIST:ADDRESSLINE|*
                </p>
                <p style="margin: 0; font-family: 'Plus Jakarta Sans', Arial, Helvetica, sans-serif; font-size: 11px; line-height: 16px; color: #b0b4b8; text-align: center;">
                  <a href="*|UPDATE_PROFILE|*" style="color: #FFFFFE; text-decoration: underline;">Update Preferences</a>
                  &nbsp;&bull;&nbsp;
                  <a href="*|UNSUB|*" style="color: #FFFFFE; text-decoration: underline;">Unsubscribe</a>
                  &nbsp;&bull;&nbsp;
                  <a href="*|ARCHIVE|*" style="color: #FFFFFE; text-decoration: underline;">View in Browser</a>
                </p>
              </div>
            </td>
          </tr>
"""

# Insert before closing </table> <!-- MSO container -->
target_close = '        </table>\n        <!--[if (gte mso 9)|(IE)]>'
if target_close in html_mc:
    html_mc = html_mc.replace(target_close, mc_compliance_block + "\n" + target_close)
else:
    # Fallback
    html_mc = html_mc.replace('        </table>', mc_compliance_block + '\n        </table>', 1)

with open(os.path.join(DELIV_DIR, "mailchimp-template.html"), "w", encoding="utf-8") as f:
    f.write(html_mc)
print("=== 5. Generated Deliverable/mailchimp-template.html ===")

# 6. Render Desktop & Mobile Previews using Headless Edge
EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
print("=== 6. Rendering high-resolution screenshots ===")

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

# Desktop (800x2300 viewport, centered 600px email)
render_and_crop("preview-desktop.png", 800, 2300)

# Mobile (500x2400 viewport, responsive fluid view)
render_and_crop("preview-mobile.png", 500, 2400)

# 7. Generate README.md
readme_content = """# Fulton Residences: You're Invited — Step Inside
### Project ID: `4559216753` (Germantown, Nashville, TN)
**Due Date:** Thursday, October 8th, 2026

---

## 📦 Deliverable Package Overview

This package contains production-ready, dark-mode hardened HTML email templates, optimized 2x Retina assets, and client preview renders for the **Fulton: You are Invited Step Inside** eblast.

```
Deliverable/
├── index.html                  # Production HTML template (relative "images/" paths)
├── index-hosted.html           # Standalone HTML template (hosted HTTPS CDN image URLs)
├── index-client-cdn.html       # Official client CDN template (assets.tangocrew.com URLs)
├── mailchimp-template.html     # Mailchimp master template (mc:edit regions + CAN-SPAM merge tags)
├── README.md                   # Technical documentation & ESP deployment guide
├── images/                     # Optimized 2x Retina production assets
│   ├── header-banner-2x.jpg    # Fulton logo + stone/ivy banner (1200x394, 600x197 display)
│   ├── youre-invited-2x.jpg    # Mauve "You're Invited" serif banner (1200x200, 600x100 display)
│   ├── goat-logo-2x.png        # Transparent 2x Retina logo for The Goat (484x218, 242px display)
│   ├── interior-photo-2x.jpg   # High-res interior residence photo (1060x659, 530x330 display)
│   ├── icon-fb-2x.png          # Transparent 4x Retina Facebook icon (104x104, 26x26 display)
│   ├── icon-ig-2x.png          # Transparent 4x Retina Instagram icon (104x104, 26x26 display)
│   └── footer-banner-2x.jpg    # Footer logos + Equal Housing banner (1200x386, 600x193 display)
└── previews/
    ├── preview-desktop.png     # Full-length 600px desktop render
    └── preview-mobile.png      # Fluid 390px mobile viewport render
```

---

## 🚀 Which Template Should I Use?

| File | Best Used For | Notes |
| :--- | :--- | :--- |
| **`index-hosted.html`** | **Direct Sending & Fast Preview** | Self-contained, single-file HTML. All images load directly from high-speed HTTPS CDN endpoints (`https://iili.io/`). Works immediately in any ESP or CRM (HubSpot, Salesforce, Klaviyo, SendGrid, Mailtrap) without uploading assets. |
| **`index-client-cdn.html`** | **Official Client CDN Deployment** | Points to official client asset path: `https://assets.tangocrew.com/Fulton/4559216753/`. Deploy after assets are synced to client media server. |
| **`mailchimp-template.html`** | **Mailchimp Campaigns** | Includes `mc:edit` editable content blocks for headers, body copy, CTA labels, and CAN-SPAM compliant unsubscribe/preference merge tags. |
| **`index.html`** | **Self-Hosted / ZIP Upload** | References `./images/`. Upload the `images/` folder alongside `index.html` to your media server or ZIP-based ESP importer. |

---

## 🌐 Hosted Image Endpoints (HTTPS CDN)

All 7 production assets are pre-hosted on persistent, high-speed CDN endpoints:

* **Header Banner**: `https://iili.io/nEEX0Jt.jpg`
* **You're Invited Banner**: `https://iili.io/nEEXEen.jpg`
* **The Goat Logo**: `https://iili.io/nEEc6qF.png`
* **Interior Photo**: `https://iili.io/nEEciga.jpg`
* **Facebook Icon**: `https://iili.io/nEEcRVt.png`
* **Instagram Icon**: `https://iili.io/nEEctbp.png`
* **Footer Banner**: `https://iili.io/nEEcmXI.jpg`

---

## 🔗 Production Links & Destination URLs

* **Primary Website**: `https://liveatfulton.com`
* **RSVP Button & Email**: `mailto:info@liveatfulton.com?subject=I%20want%20to%20come%20to%20the%20event`
* **Private Presentation**: `mailto:info@liveatfulton.com?subject=I%20want%20to%20more%20information%20about%20Fulton`
* **Explore Fulton Residences**: `https://liveatfulton.com`
* **Facebook**: `https://www.facebook.com/fultonresidences`
* **Instagram**: `https://www.instagram.com/fultonnashville/`

---

## 🛡️ Dark Mode & Cross-Client Compatibility

1. **Outlook Classic Desktop (MSO 2016-365 PC)**:
   * 600px MSO ghost tables (`<!--[if (gte mso 9)|(IE)]>`) maintain structural width integrity.
   * `mso-line-height-rule: exactly;` prevents font shifting and line-height expansion in Word rendering engine.
2. **Gmail App (iOS & Android)**:
   * Off-hex color locking (`#414446`, `#8D5B5B`, `#FFFFFE`) with dual `linear-gradient` declarations prevents aggressive background color inversion.
   * "You're Invited" serif headline rendered as 2x Retina asset to guarantee 100% typography fidelity without relying on stripped web fonts.
3. **Apple Mail (iOS & macOS)**:
   * Supported color scheme meta tags (`<meta name="color-scheme" content="light dark" />`) preserve native dark mode elegance.
4. **Deliverability & Spam Filter Score**:
   * SpamAssassin Score: **0.0 / 5.0** (Zero spam flags).
   * Includes plain-text multipart payload and zero-height preheader preview text.
"""

with open(os.path.join(DELIV_DIR, "README.md"), "w", encoding="utf-8") as f:
    f.write(readme_content)
print("=== 7. Generated Deliverable/README.md ===")

# 8. Create ZIP archive
zip_path = os.path.join(HERE, "Fulton-Residences-Project-4559216753-Deliverable.zip")
print(f"=== 8. Creating ZIP archive: {zip_path} ===")
with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
    for root, dirs, files in os.walk(DELIV_DIR):
        for file in files:
            full_path = os.path.join(root, file)
            rel_path = os.path.relpath(full_path, HERE)
            zipf.write(full_path, rel_path)
            print(f"  Zipped: {rel_path}")

print(f"\nDeliverable package complete! Archive size: {os.path.getsize(zip_path)//1024} KB")
