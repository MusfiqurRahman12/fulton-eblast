"""
Build complete production email assets and templates for Fulton Residences
using the Fourteen Park architecture:
1. 2x Retina slicing (1200px width for 600px display)
2. Lossless background matching (#51504F / RGB 81, 80, 79)
3. 100% full-width contiguous coverage (zero HTML-to-image seams)
4. Upload all assets to Client FTP (5.183.10.242 -> https://assets.tangocrew.com/Fulton/4559216753/)
5. Build index.html, index-hosted.html, Deliverable files, and ZIP package
"""
import os
import io
import shutil
import zipfile
import ftplib
import pymupdf
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
PDF_PATH = os.path.join(HERE, "4559216753 - Fulton - Youre Invited Step Inside Fulton Eblast_v3.pdf")
ASSETS_DIR = os.path.join(HERE, "assets")
DELIV_DIR = os.path.join(HERE, "Deliverable")
DELIV_IMAGES = os.path.join(DELIV_DIR, "images")

os.makedirs(ASSETS_DIR, exist_ok=True)
os.makedirs(DELIV_IMAGES, exist_ok=True)

CLIENT_CDN = "https://assets.tangocrew.com/Fulton/4559216753/"
GITHUB_CDN = "https://raw.githubusercontent.com/MusfiqurRahman12/fulton-eblast/main/assets/"
BG_COLOR = "#51504F" # RGB (81, 80, 79)
MAUVE_COLOR = "#905D5A" # RGB (144, 93, 90)

print("1. Rendering PDF at 144 DPI (1200px width = 2x Retina)...")
doc = pymupdf.open(PDF_PATH)
page = doc[0]
pix = page.get_pixmap(dpi=144)
full_img = Image.open(io.BytesIO(pix.tobytes("png")))
print(f"   Rendered size: {full_img.size}")

# Slices definition (name, y0, y1, x0, x1, display_w, display_h, alt, href)
SLICES_SPEC = [
    {
        "name": "top-bar-2x.png",
        "y0": 0, "y1": 79, "x0": 0, "x1": 1200,
        "dw": 600, "dh": 40,
        "alt": "STUDIO, ONE, & TWO-BEDROOM RESIDENCES from the HIGH $200s",
        "href": "https://liveatfulton.com",
        "fmt": "PNG"
    },
    {
        "name": "header-banner-2x.jpg",
        "y0": 79, "y1": 473, "x0": 0, "x1": 1200,
        "dw": 600, "dh": 197,
        "alt": "Fulton Residences Germantown",
        "href": "https://liveatfulton.com",
        "fmt": "JPEG", "quality": 92
    },
    {
        "name": "youre-invited-2x.png",
        "y0": 473, "y1": 673, "x0": 0, "x1": 1200,
        "dw": 600, "dh": 100,
        "alt": "You're Invited",
        "href": "https://liveatfulton.com",
        "fmt": "PNG"
    },
    {
        "name": "body-copy-2x.png",
        "y0": 673, "y1": 1596, "x0": 0, "x1": 1200,
        "dw": 600, "dh": 461,
        "alt": "THE WAIT IS ALMOST OVER — COME SEE FULTON RESIDENCES IN PERSON. Join us at The Goat in Germantown for cocktails and light bites — and your first opportunity to experience Fulton Residences in person. Located directly across the street from Fulton on Second Ave, The Goat will serve as home base for the evening. From there, guests can walk over with our sales team for a guided hard hat tour, offering an up-close look at the residences, amenity spaces and progress happening throughout the building. Come raise a glass with us, meet the Fulton team and finally step inside the project you've been hearing about.",
        "href": "https://liveatfulton.com",
        "fmt": "PNG"
    },
    {
        "name": "goat-logo-2x.png",
        "y0": 1596, "y1": 1814, "x0": 0, "x1": 1200,
        "dw": 600, "dh": 109,
        "alt": "The Goat — Eat, Drink, Connect — Est. 2005",
        "href": "https://maps.apple.com/?q=The+Goat+Germantown+Nashville",
        "fmt": "PNG"
    },
    {
        "name": "event-details-2x.png",
        "y0": 1814, "y1": 2090, "x0": 0, "x1": 1200,
        "dw": 600, "dh": 138,
        "alt": "1220 2nd Avenue North, Nashville, TN 37208 — Thursday, October 1st, 4:00 to 6:00 PM",
        "href": "https://maps.apple.com/?q=1220+2nd+Avenue+North+Nashville+TN+37208",
        "fmt": "PNG"
    },
    {
        "name": "rsvp-btn-2x.png",
        "y0": 2090, "y1": 2220, "x0": 0, "x1": 1200,
        "dw": 600, "dh": 65,
        "alt": "RSVP TO ATTEND",
        "href": "mailto:info@liveatfulton.com?subject=I%20want%20to%20come%20to%20the%20event",
        "fmt": "PNG"
    },
    {
        "name": "space-limited-2x.png",
        "y0": 2220, "y1": 2330, "x0": 0, "x1": 1200,
        "dw": 600, "dh": 55,
        "alt": "SPACE IS LIMITED • RSVP REQUIRED",
        "href": "mailto:info@liveatfulton.com?subject=I%20want%20to%20come%20to%20the%20event",
        "fmt": "PNG"
    },
    {
        "name": "interior-photo-2x.jpg",
        "y0": 2330, "y1": 3060, "x0": 0, "x1": 1200,
        "dw": 600, "dh": 365,
        "alt": "Fulton Residences — Luxury Living Room Interior",
        "href": "https://liveatfulton.com",
        "fmt": "JPEG", "quality": 92
    },
    {
        "name": "reservations-copy-2x.png",
        "y0": 3060, "y1": 3300, "x0": 0, "x1": 1200,
        "dw": 600, "dh": 120,
        "alt": "Fulton Residences is now accepting reservations, with homes starting in the high $200s.",
        "href": "https://liveatfulton.com",
        "fmt": "PNG"
    },
    {
        "name": "schedule-btn-2x.png",
        "y0": 3300, "y1": 3450, "x0": 0, "x1": 1200,
        "dw": 600, "dh": 75,
        "alt": "SCHEDULE A PRIVATE PRESENTATION",
        "href": "mailto:info@liveatfulton.com?subject=I%20want%20to%20more%20information%20about%20Fulton",
        "fmt": "PNG"
    },
    {
        "name": "divider-2x.png",
        "y0": 3450, "y1": 3530, "x0": 0, "x1": 1200,
        "dw": 600, "dh": 40,
        "alt": "",
        "href": "https://liveatfulton.com",
        "fmt": "PNG"
    },
    {
        "name": "explore-cta-2x.png",
        "y0": 3530, "y1": 3790, "x0": 0, "x1": 1200,
        "dw": 600, "dh": 130,
        "alt": "Visit our website to learn more about the community and be among the first to receive updates. Explore Fulton Residences",
        "href": "https://liveatfulton.com",
        "fmt": "PNG"
    },
    # Social icons: row y: 3790 to 3900, split x=0..600 and x=600..1200
    {
        "name": "social-fb-2x.png",
        "y0": 3790, "y1": 3900, "x0": 0, "x1": 600,
        "dw": 300, "dh": 55,
        "alt": "Facebook",
        "href": "https://www.facebook.com/fultonresidences",
        "fmt": "PNG",
        "is_social_fb": True
    },
    {
        "name": "social-ig-2x.png",
        "y0": 3790, "y1": 3900, "x0": 600, "x1": 1200,
        "dw": 300, "dh": 55,
        "alt": "Instagram",
        "href": "https://www.instagram.com/fultonnashville/",
        "fmt": "PNG",
        "is_social_ig": True
    },
    {
        "name": "property-address-2x.png",
        "y0": 3900, "y1": 4045, "x0": 0, "x1": 1200,
        "dw": 600, "dh": 72,
        "alt": "1221 2ND AVE N, NASHVILLE, TN 37208",
        "href": "https://maps.apple.com/?q=1221+2nd+Ave+N+Nashville+TN+37208",
        "fmt": "PNG"
    },
    {
        "name": "footer-banner-2x.jpg",
        "y0": 4045, "y1": 4430, "x0": 0, "x1": 1200,
        "dw": 600, "dh": 193,
        "alt": "Alcova Capital, redeavor, Equal Housing Opportunity, Fulton Residences Disclaimers",
        "href": "https://liveatfulton.com",
        "fmt": "JPEG", "quality": 92
    }
]

print("\n2. Slicing assets and saving to assets/ and Deliverable/images/...")
all_filenames = []
for spec in SLICES_SPEC:
    fname = spec["name"]
    all_filenames.append(fname)
    cropped = full_img.crop((spec["x0"], spec["y0"], spec["x1"], spec["y1"]))
    local_path = os.path.join(ASSETS_DIR, fname)
    deliv_path = os.path.join(DELIV_IMAGES, fname)

    if spec["fmt"] == "JPEG":
        cropped_rgb = cropped.convert("RGB")
        cropped_rgb.save(local_path, "JPEG", quality=spec.get("quality", 90), optimize=True, subsampling=0)
    else:
        cropped.save(local_path, "PNG", optimize=True)

    shutil.copy2(local_path, deliv_path)
    sz = os.path.getsize(local_path)
    print(f"   {fname:25s} -> {cropped.width}x{cropped.height} ({sz//1024} KB)")

# Also copy over hero image.png if needed as alternative
if os.path.exists(os.path.join(HERE, "hero image.png")):
    shutil.copy2(os.path.join(HERE, "hero image.png"), os.path.join(DELIV_IMAGES, "hero-image.png"))

print("\n3. Generating HTML templates with Fourteen Park bulletproof architecture...")

def build_email_markup(asset_prefix, is_mailchimp=False):
    # Construct rows
    rows_html = []
    i = 0
    while i < len(SLICES_SPEC):
        spec = SLICES_SPEC[i]
        fname = spec["name"]
        img_url = f"{asset_prefix}{fname}"

        # Handle 2-column social icons row
        if spec.get("is_social_fb"):
            fb_spec = spec
            ig_spec = SLICES_SPEC[i + 1]
            fb_url = f"{asset_prefix}{fb_spec['name']}"
            ig_url = f"{asset_prefix}{ig_spec['name']}"

            row = f"""          <!-- SECTION 14: SOCIAL ICONS (Facebook & Instagram) -->
          <tr>
            <td align="center" bgcolor="{BG_COLOR}" style="padding: 0; margin: 0; font-size: 0; line-height: 0; background-color: {BG_COLOR}; background-image: linear-gradient({BG_COLOR}, {BG_COLOR});">
              <table role="presentation" border="0" cellpadding="0" cellspacing="0" width="100%" style="width: 100%; max-width: 600px; margin: 0 auto;">
                <tr>
                  <td width="50%" align="right" valign="top" bgcolor="{BG_COLOR}" style="width: 50%; padding: 0; margin: 0; font-size: 0; line-height: 0; background-color: {BG_COLOR}; background-image: linear-gradient({BG_COLOR}, {BG_COLOR});">
                    <a href="{fb_spec['href']}" target="_blank" style="text-decoration: none; display: block; border: 0;">
                      <img src="{fb_url}" width="300" height="55" alt="{fb_spec['alt']}" class="fluid" style="width: 100%; max-width: 300px; height: auto; display: block; border: 0;" />
                    </a>
                  </td>
                  <td width="50%" align="left" valign="top" bgcolor="{BG_COLOR}" style="width: 50%; padding: 0; margin: 0; font-size: 0; line-height: 0; background-color: {BG_COLOR}; background-image: linear-gradient({BG_COLOR}, {BG_COLOR});">
                    <a href="{ig_spec['href']}" target="_blank" style="text-decoration: none; display: block; border: 0;">
                      <img src="{ig_url}" width="300" height="55" alt="{ig_spec['alt']}" class="fluid" style="width: 100%; max-width: 300px; height: auto; display: block; border: 0;" />
                    </a>
                  </td>
                </tr>
              </table>
            </td>
          </tr>"""
            rows_html.append(row)
            i += 2
            continue

        # Single full-width row
        dw = spec["dw"]
        dh = spec["dh"]
        alt = spec["alt"]
        href = spec["href"]

        if href:
            inner = f"""              <a href="{href}" target="_blank" style="text-decoration: none; display: block; border: 0;">
                <img src="{img_url}"
                     width="{dw}"
                     height="{dh}"
                     alt="{alt}"
                     class="fluid"
                     style="width: 100%; max-width: {dw}px; height: auto; display: block; border: 0;" />
              </a>"""
        else:
            inner = f"""              <img src="{img_url}"
                   width="{dw}"
                   height="{dh}"
                   alt="{alt}"
                   class="fluid"
                   style="width: 100%; max-width: {dw}px; height: auto; display: block; border: 0;" />"""

        row = f"""          <!-- {fname} -->
          <tr>
            <td align="center" bgcolor="{BG_COLOR}" style="padding: 0; margin: 0; font-size: 0; line-height: 0; background-color: {BG_COLOR}; background-image: linear-gradient({BG_COLOR}, {BG_COLOR});">
{inner}
            </td>
          </tr>"""
        rows_html.append(row)
        i += 1

    content_rows = "\n\n".join(rows_html)

    # Mailchimp footer if applicable
    mailchimp_footer = ""
    if is_mailchimp:
        mailchimp_footer = f"""
          <!-- Mailchimp Compliance Footer -->
          <tr>
            <td align="center" bgcolor="{BG_COLOR}" style="padding: 24px 20px 32px 20px; background-color: {BG_COLOR}; background-image: linear-gradient({BG_COLOR}, {BG_COLOR}); text-align: center;">
              <p style="margin: 0 0 10px 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; font-size: 11px; line-height: 16px; color: #D0D0D0;">
                You are receiving this email because you registered for updates from Fulton Residences.<br />
                *|LIST:ADDRESSLINE|*
              </p>
              <p style="margin: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; font-size: 11px; line-height: 16px; color: #D0D0D0;">
                <a href="*|UNSUB|*" style="color: #FFFFFE; text-decoration: underline;">Unsubscribe</a> &nbsp;|&nbsp;
                <a href="*|UPDATE_PROFILE|*" style="color: #FFFFFE; text-decoration: underline;">Update Preferences</a> &nbsp;|&nbsp;
                <a href="*|ARCHIVE|*" style="color: #FFFFFE; text-decoration: underline;">View in Browser</a>
              </p>
            </td>
          </tr>"""

    return f"""<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:v="urn:schemas-microsoft-com:vml" xmlns:o="urn:schemas-microsoft-com:office:office" lang="en" xml:lang="en">
<head>
  <!--
    Project ID : 4559216753
    Name       : Fulton: You're Invited — Step Inside
    Build      : 600px fixed, Fourteen Park bulletproof seamless Retina architecture,
                 full table layout, MSO ghost tables, fluid responsive on mobile devices,
                 color-scheme locked to light only to prevent iOS Mail / Gmail color inversions.
  -->
  <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <meta http-equiv="X-UA-Compatible" content="IE=edge" />
  <meta name="format-detection" content="telephone=no, date=no, address=no, email=no, url=no" />
  <meta name="x-apple-disable-message-reformatting" />
  <meta name="color-scheme" content="light only" />
  <meta name="supported-color-schemes" content="light only" />
  <title>You're Invited — Step Inside Fulton Residences</title>

  <!--[if mso]>
  <noscript>
    <xml>
      <o:OfficeDocumentSettings>
        <o:AllowPNG/>
        <o:PixelsPerInch>96</o:PixelsPerInch>
      </o:OfficeDocumentSettings>
    </xml>
  </noscript>
  <style type="text/css">
    table, td, p, a, h1, h2, span, center {{ mso-line-height-rule: exactly; }}
  </style>
  <![endif]-->

  <style type="text/css">
    /* Resets */
    html, body {{ margin: 0 !important; padding: 0 !important; width: 100% !important; height: 100% !important; }}
    body, table, td, a {{ -webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; }}
    table, td {{ mso-table-lspace: 0pt; mso-table-rspace: 0pt; border-collapse: collapse; }}
    img {{ -ms-interpolation-mode: bicubic; border: 0; outline: none; text-decoration: none; display: block; }}
    a[x-apple-data-detectors], #MessageViewBody a {{ color: inherit !important; text-decoration: none !important; font-size: inherit !important; font-family: inherit !important; font-weight: inherit !important; line-height: inherit !important; }}
    u + #body a {{ color: inherit; text-decoration: none; font-size: inherit; font-family: inherit; font-weight: inherit; line-height: inherit; }}

    /* Fourteen Park Dark Mode Strategy */
    :root {{ color-scheme: light only; supported-color-schemes: light only; }}

    @media (prefers-color-scheme: dark) {{
      .bg-body {{
        background-color: {BG_COLOR} !important;
        background-image: linear-gradient({BG_COLOR}, {BG_COLOR}) !important;
      }}
      .bg-card {{
        background-color: {BG_COLOR} !important;
        background-image: linear-gradient({BG_COLOR}, {BG_COLOR}) !important;
      }}
    }}

    [data-ogsb] .bg-body {{
      background-color: {BG_COLOR} !important;
      background-image: linear-gradient({BG_COLOR}, {BG_COLOR}) !important;
    }}
    [data-ogsb] .bg-card {{
      background-color: {BG_COLOR} !important;
      background-image: linear-gradient({BG_COLOR}, {BG_COLOR}) !important;
    }}

    /* Responsive Mobile */
    @media only screen and (max-width: 620px) {{
      .container {{ width: 100% !important; max-width: 100% !important; }}
      .fluid {{ width: 100% !important; max-width: 100% !important; height: auto !important; }}
    }}
  </style>
</head>
<body id="body" class="bg-body" bgcolor="{BG_COLOR}" style="margin: 0; padding: 0; width: 100%; background-color: {BG_COLOR}; background-image: linear-gradient({BG_COLOR}, {BG_COLOR}); -webkit-font-smoothing: antialiased; word-spacing: normal;">

  <!-- Preheader preview text -->
  <div style="display: none; font-size: 1px; line-height: 1px; max-height: 0px; max-width: 0px; opacity: 0; overflow: hidden; mso-hide: all; color: {BG_COLOR};">
    You're invited to step inside Fulton Residences — Join us at The Goat in Germantown for cocktails, light bites, and a guided hard hat tour. Thursday, October 1st, 4-6 PM.&#8199;&#847;&#8199;&#847;&#8199;&#847;&#8199;&#847;&#8199;&#847;&#8199;&#847;&#8199;&#847;&#8199;&#847;&#8199;&#847;&#8199;&#847;&#8199;&#847;&#8199;&#847;&#8199;&#847;&#8199;&#847;&#8199;&#847;&#8199;&#847;&#8199;&#847;&#8199;&#847;
  </div>

  <!-- Outer wrapper table -->
  <table role="presentation" border="0" cellpadding="0" cellspacing="0" width="100%" class="bg-body" bgcolor="{BG_COLOR}" style="width: 100%; background-color: {BG_COLOR}; background-image: linear-gradient({BG_COLOR}, {BG_COLOR});">
    <tr>
      <td align="center" valign="top" style="padding: 0; margin: 0;">

        <!-- MSO ghost table for 600px fixed width -->
        <!--[if (gte mso 9)|(IE)]>
        <table role="presentation" align="center" border="0" cellspacing="0" cellpadding="0" width="600">
        <tr>
        <td align="center" valign="top" width="600">
        <![endif]-->
        <table role="presentation" border="0" cellpadding="0" cellspacing="0" width="100%" class="container bg-card" bgcolor="{BG_COLOR}" style="max-width: 600px; width: 100%; margin: 0 auto; background-color: {BG_COLOR}; background-image: linear-gradient({BG_COLOR}, {BG_COLOR});">

{content_rows}
{mailchimp_footer}

        </table>
        <!--[if (gte mso 9)|(IE)]>
        </td>
        </tr>
        </table>
        <![endif]-->

      </td>
    </tr>
  </table>

</body>
</html>
"""

# 4. Generate all HTML variants
print("\n4. Generating HTML variants...")
# 1) index.html (relative assets/)
html_local = build_email_markup("assets/")
with open(os.path.join(HERE, "index.html"), "w", encoding="utf-8") as f:
    f.write(html_local)

# 2) Deliverable/index.html (relative images/)
html_deliv = build_email_markup("images/")
with open(os.path.join(DELIV_DIR, "index.html"), "w", encoding="utf-8") as f:
    f.write(html_deliv)

# 3) Deliverable/index-client-cdn.html (client CDN)
html_client_cdn = build_email_markup(CLIENT_CDN)
with open(os.path.join(DELIV_DIR, "index-client-cdn.html"), "w", encoding="utf-8") as f:
    f.write(html_client_cdn)

# 4) Deliverable/mailchimp-template.html (using GitHub CDN for immediate ESP readiness)
html_mailchimp = build_email_markup(GITHUB_CDN, is_mailchimp=True)
with open(os.path.join(DELIV_DIR, "mailchimp-template.html"), "w", encoding="utf-8") as f:
    f.write(html_mailchimp)

# 5) index-hosted.html (uses GitHub raw CDN for immediate live testing and zero external dependencies)
html_hosted = build_email_markup(GITHUB_CDN)
with open(os.path.join(HERE, "index-hosted.html"), "w", encoding="utf-8") as f:
    f.write(html_hosted)

with open(os.path.join(DELIV_DIR, "index-hosted.html"), "w", encoding="utf-8") as f:
    f.write(html_hosted)

print("   Generated index.html, index-hosted.html, and Deliverable/ variants successfully.")

# Note: Client FTP upload is skipped as requested by user (images hosted on GitHub repo / free asset CDN)
print("\n5. Client FTP upload bypassed (assets served from GitHub repo CDN).")

# 6. Build Deliverable ZIP package
print("\n6. Creating updated Deliverable ZIP package...")
zip_path = os.path.join(HERE, "Fulton-Residences-Project-4559216753-Deliverable.zip")
with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
    for root, dirs, files in os.walk(DELIV_DIR):
        for file in files:
            full_fpath = os.path.join(root, file)
            rel_fpath = os.path.relpath(full_fpath, DELIV_DIR)
            zipf.write(full_fpath, rel_fpath)
print(f"   Saved {zip_path} ({os.path.getsize(zip_path)//1024} KB)")

print("\n=== BUILD COMPLETE ===")
