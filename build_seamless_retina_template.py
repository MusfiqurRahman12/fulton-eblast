import os
import json
import shutil
import zipfile
import subprocess
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
DELIV_DIR = os.path.join(HERE, "Deliverable")
IMAGES_DIR = os.path.join(DELIV_DIR, "images")
PREVIEWS_DIR = os.path.join(DELIV_DIR, "previews")

os.makedirs(IMAGES_DIR, exist_ok=True)
os.makedirs(PREVIEWS_DIR, exist_ok=True)

with open(os.path.join(HERE, "hosted_assets.json"), "r") as f:
    hosted_map = json.load(f)

CLIENT_CDN = "https://assets.tangocrew.com/Fulton/4559216753/"

# All assets list
ALL_ASSETS = [
    "top-bar-2x.jpg",
    "header-banner-2x.jpg",
    "youre-invited-2x.jpg",
    "body-copy-2x.jpg",
    "goat-logo-2x.png",
    "event-details-2x.jpg",
    "rsvp-btn-2x.jpg",
    "space-limited-2x.jpg",
    "interior-photo-2x.jpg",
    "reservations-copy-2x.jpg",
    "schedule-btn-2x.jpg",
    "divider-2x.jpg",
    "explore-cta-2x.jpg",
    "icon-fb-2x.png",
    "icon-ig-2x.png",
    "property-address-2x.jpg",
    "footer-banner-2x.jpg"
]

# Copy all assets to Deliverable/images/
for fname in ALL_ASSETS:
    src = os.path.join(HERE, "assets", fname)
    dst = os.path.join(IMAGES_DIR, fname)
    shutil.copy2(src, dst)

def generate_html(asset_prefix_or_map):
    def get_url(fname):
        if isinstance(asset_prefix_or_map, dict):
            return asset_prefix_or_map.get(f"assets/{fname}", f"assets/{fname}")
        else:
            return f"{asset_prefix_or_map}{fname}"

    u_topbar = get_url("top-bar-2x.jpg")
    u_header = get_url("header-banner-2x.jpg")
    u_invited = get_url("youre-invited-2x.jpg")
    u_body = get_url("body-copy-2x.jpg")
    u_goat = get_url("goat-logo-2x.png")
    u_event = get_url("event-details-2x.jpg")
    u_rsvp = get_url("rsvp-btn-2x.jpg")
    u_space = get_url("space-limited-2x.jpg")
    u_interior = get_url("interior-photo-2x.jpg")
    u_reserv = get_url("reservations-copy-2x.jpg")
    u_sched = get_url("schedule-btn-2x.jpg")
    u_div = get_url("divider-2x.jpg")
    u_explore = get_url("explore-cta-2x.jpg")
    u_fb = get_url("icon-fb-2x.png")
    u_ig = get_url("icon-ig-2x.png")
    u_prop = get_url("property-address-2x.jpg")
    u_footer = get_url("footer-banner-2x.jpg")

    return f"""<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:v="urn:schemas-microsoft-com:vml" xmlns:o="urn:schemas-microsoft-com:office:office" lang="en" xml:lang="en">
<head>
  <!--
    Project ID : 4559216753
    Name       : Fulton: You're Invited — Step Inside
    Build      : 600px fixed, seamless Retina-sliced architecture (zero dark-mode inversion bugs),
                 full table layout, MSO ghost tables, fluid responsive on mobile devices.
  -->
  <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <meta http-equiv="X-UA-Compatible" content="IE=edge" />
  <meta name="format-detection" content="telephone=no, date=no, address=no, email=no, url=no" />
  <meta name="x-apple-disable-message-reformatting" />
  <meta name="color-scheme" content="light dark" />
  <meta name="supported-color-schemes" content="light dark" />
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

    /* Responsive Mobile */
    @media only screen and (max-width: 620px) {{
      .container {{ width: 100% !important; max-width: 100% !important; }}
      .fluid {{ width: 100% !important; max-width: 100% !important; height: auto !important; }}
      .p-mob-photo {{ padding-left: 20px !important; padding-right: 20px !important; }}
    }}
  </style>
</head>
<body id="body" bgcolor="#414446" style="margin: 0; padding: 0; width: 100%; background-color: #414446; background-image: linear-gradient(#414446, #414446); -webkit-font-smoothing: antialiased; word-spacing: normal;">

  <!-- Preheader preview text -->
  <div style="display: none; font-size: 1px; line-height: 1px; max-height: 0px; max-width: 0px; opacity: 0; overflow: hidden; mso-hide: all; color: #414446;">
    You're invited to step inside Fulton Residences — Join us at The Goat in Germantown for cocktails, light bites, and a guided hard hat tour. Thursday, October 1st, 4-6 PM.&#8199;&#847;&#8199;&#847;&#8199;&#847;&#8199;&#847;&#8199;&#847;&#8199;&#847;&#8199;&#847;&#8199;&#847;&#8199;&#847;&#8199;&#847;&#8199;&#847;&#8199;&#847;&#8199;&#847;&#8199;&#847;&#8199;&#847;&#8199;&#847;&#8199;&#847;&#8199;&#847;
  </div>

  <!-- Outer wrapper table -->
  <table role="presentation" border="0" cellpadding="0" cellspacing="0" width="100%" bgcolor="#414446" style="width: 100%; background-color: #414446; background-image: linear-gradient(#414446, #414446);">
    <tr>
      <td align="center" valign="top" style="padding: 0; margin: 0;">

        <!-- MSO ghost table for 600px fixed width -->
        <!--[if (gte mso 9)|(IE)]>
        <table role="presentation" align="center" border="0" cellspacing="0" cellpadding="0" width="600">
        <tr>
        <td align="center" valign="top" width="600">
        <![endif]-->
        <table role="presentation" border="0" cellpadding="0" cellspacing="0" width="100%" class="container" style="max-width: 600px; width: 100%; margin: 0 auto;">

          <!-- SECTION 1: TOP PRICING BAR -->
          <tr>
            <td align="center" bgcolor="#8D5B5B" style="padding: 0; margin: 0; font-size: 0; line-height: 0; background-color: #8D5B5B;">
              <img src="{u_topbar}"
                   width="600"
                   height="39"
                   alt="STUDIO, ONE, &amp; TWO-BEDROOM RESIDENCES from the HIGH $200s"
                   class="fluid"
                   style="width: 100%; max-width: 600px; height: auto; display: block; border: 0;" />
            </td>
          </tr>

          <!-- SECTION 2: HEADER BANNER (Fulton Logo + Stone/Ivy) -->
          <tr>
            <td align="center" style="padding: 0; margin: 0; font-size: 0; line-height: 0;">
              <a href="https://liveatfulton.com" target="_blank" style="text-decoration: none; display: block;">
                <img src="{u_header}"
                     width="600"
                     height="197"
                     alt="Fulton Residences Germantown"
                     class="fluid"
                     style="width: 100%; max-width: 600px; height: auto; display: block; border: 0;" />
              </a>
            </td>
          </tr>

          <!-- SECTION 3: "YOU'RE INVITED" MAUVE BANNER -->
          <tr>
            <td align="center" bgcolor="#8D5B5B" style="padding: 0; margin: 0; font-size: 0; line-height: 0; background-color: #8D5B5B;">
              <img src="{u_invited}"
                   width="600"
                   height="100"
                   alt="You're Invited"
                   class="fluid"
                   style="width: 100%; max-width: 600px; height: auto; display: block; border: 0;" />
            </td>
          </tr>

          <!-- SECTION 4: BODY COPY (Event Invitation) -->
          <tr>
            <td align="center" bgcolor="#414446" style="padding: 0; margin: 0; font-size: 0; line-height: 0; background-color: #414446; background-image: linear-gradient(#414446, #414446);">
              <img src="{u_body}"
                   width="600"
                   height="438"
                   alt="THE WAIT IS ALMOST OVER — COME SEE FULTON RESIDENCES IN PERSON. Join us at The Goat in Germantown for cocktails and light bites — and your first opportunity to experience Fulton Residences in person. Located directly across the street from Fulton on Second Ave, The Goat will serve as home base for the evening. From there, guests can walk over with our sales team for a guided hard hat tour, offering an up-close look at the residences, amenity spaces and progress happening throughout the building. Come raise a glass with us, meet the Fulton team and finally step inside the project you've been hearing about."
                   class="fluid"
                   style="width: 100%; max-width: 600px; height: auto; display: block; border: 0;" />
            </td>
          </tr>

          <!-- SECTION 5: THE GOAT LOGO -->
          <tr>
            <td align="center" bgcolor="#414446" style="padding: 10px 40px 10px 40px; background-color: #414446; background-image: linear-gradient(#414446, #414446);">
              <img src="{u_goat}"
                   width="242"
                   alt="The Goat — Eat, Drink, Connect — Est. 2005"
                   style="width: 242px; max-width: 100%; height: auto; display: block; margin: 0 auto; border: 0;" />
            </td>
          </tr>

          <!-- SECTION 6: EVENT DETAILS (Address + Date/Time) -->
          <tr>
            <td align="center" bgcolor="#414446" style="padding: 0; margin: 0; font-size: 0; line-height: 0; background-color: #414446; background-image: linear-gradient(#414446, #414446);">
              <a href="https://maps.apple.com/?q=1220+2nd+Avenue+North+Nashville+TN+37208" target="_blank" style="text-decoration: none; display: block;">
                <img src="{u_event}"
                     width="600"
                     height="120"
                     alt="1220 2nd Avenue North, Nashville, TN 37208 — Thursday, October 1st, 4:00 to 6:00 PM"
                     class="fluid"
                     style="width: 100%; max-width: 600px; height: auto; display: block; border: 0;" />
              </a>
            </td>
          </tr>

          <!-- SECTION 7: RSVP CTA BUTTON -->
          <tr>
            <td align="center" bgcolor="#414446" style="padding: 0; margin: 0; font-size: 0; line-height: 0; background-color: #414446; background-image: linear-gradient(#414446, #414446);">
              <a href="mailto:info@liveatfulton.com?subject=I%20want%20to%20come%20to%20the%20event" style="text-decoration: none; display: block;">
                <img src="{u_rsvp}"
                     width="600"
                     height="70"
                     alt="RSVP TO ATTEND"
                     class="fluid"
                     style="width: 100%; max-width: 600px; height: auto; display: block; border: 0;" />
              </a>
            </td>
          </tr>

          <!-- SECTION 7B: RSVP MICROCOPY -->
          <tr>
            <td align="center" bgcolor="#414446" style="padding: 0; margin: 0; font-size: 0; line-height: 0; background-color: #414446; background-image: linear-gradient(#414446, #414446);">
              <img src="{u_space}"
                   width="600"
                   height="40"
                   alt="SPACE IS LIMITED • RSVP REQUIRED"
                   class="fluid"
                   style="width: 100%; max-width: 600px; height: auto; display: block; border: 0;" />
            </td>
          </tr>

          <!-- SECTION 8: INTERIOR RESIDENCE PHOTO -->
          <tr>
            <td align="center" class="p-mob-photo" bgcolor="#414446" style="padding: 10px 35px 10px 35px; background-color: #414446; background-image: linear-gradient(#414446, #414446);">
              <a href="https://liveatfulton.com" target="_blank" style="text-decoration: none; border: 4px solid #8D5B5B; display: block;">
                <img src="{u_interior}"
                     width="522"
                     alt="Fulton Residences — Luxury Interior Living Room"
                     class="fluid"
                     style="width: 100%; max-width: 522px; height: auto; display: block; border: 0;" />
              </a>
            </td>
          </tr>

          <!-- SECTION 9: RESERVATIONS COPY -->
          <tr>
            <td align="center" bgcolor="#414446" style="padding: 0; margin: 0; font-size: 0; line-height: 0; background-color: #414446; background-image: linear-gradient(#414446, #414446);">
              <img src="{u_reserv}"
                   width="600"
                   height="95"
                   alt="Fulton Residences is now accepting reservations, with homes starting in the high $200s."
                   class="fluid"
                   style="width: 100%; max-width: 600px; height: auto; display: block; border: 0;" />
            </td>
          </tr>

          <!-- SECTION 10: SCHEDULE A PRIVATE PRESENTATION CTA -->
          <tr>
            <td align="center" bgcolor="#414446" style="padding: 0; margin: 0; font-size: 0; line-height: 0; background-color: #414446; background-image: linear-gradient(#414446, #414446);">
              <a href="mailto:info@liveatfulton.com?subject=I%20want%20to%20more%20information%20about%20Fulton" style="text-decoration: none; display: block;">
                <img src="{u_sched}"
                     width="600"
                     height="70"
                     alt="SCHEDULE A PRIVATE PRESENTATION"
                     class="fluid"
                     style="width: 100%; max-width: 600px; height: auto; display: block; border: 0;" />
              </a>
            </td>
          </tr>

          <!-- SECTION 11: DIVIDER -->
          <tr>
            <td align="center" bgcolor="#414446" style="padding: 0; margin: 0; font-size: 0; line-height: 0; background-color: #414446; background-image: linear-gradient(#414446, #414446);">
              <img src="{u_div}"
                   width="600"
                   height="50"
                   alt=""
                   class="fluid"
                   style="width: 100%; max-width: 600px; height: auto; display: block; border: 0;" />
            </td>
          </tr>

          <!-- SECTION 12: EXPLORE WEBSITE CTA -->
          <tr>
            <td align="center" bgcolor="#414446" style="padding: 0; margin: 0; font-size: 0; line-height: 0; background-color: #414446; background-image: linear-gradient(#414446, #414446);">
              <a href="https://liveatfulton.com" target="_blank" style="text-decoration: none; display: block;">
                <img src="{u_explore}"
                     width="600"
                     height="125"
                     alt="Visit our website to learn more about the community and be among the first to receive updates. Explore Fulton Residences"
                     class="fluid"
                     style="width: 100%; max-width: 600px; height: auto; display: block; border: 0;" />
              </a>
            </td>
          </tr>

          <!-- SECTION 13: SOCIAL ICONS (Facebook + Instagram) -->
          <tr>
            <td align="center" bgcolor="#414446" style="padding: 24px 40px 10px 40px; background-color: #414446; background-image: linear-gradient(#414446, #414446);">
              <table role="presentation" border="0" cellpadding="0" cellspacing="0" align="center">
                <tr>
                  <td align="center" style="padding: 0 22px;">
                    <a href="https://www.facebook.com/fultonresidences" target="_blank" style="text-decoration: none; display: block;">
                      <img src="{u_fb}"
                           width="26" height="26"
                           alt="Facebook"
                           style="display: block; border: 0; width: 26px; height: 26px;" />
                    </a>
                  </td>
                  <td align="center" style="padding: 0 22px;">
                    <a href="https://www.instagram.com/fultonnashville/" target="_blank" style="text-decoration: none; display: block;">
                      <img src="{u_ig}"
                           width="26" height="26"
                           alt="Instagram"
                           style="display: block; border: 0; width: 26px; height: 26px;" />
                    </a>
                  </td>
                </tr>
              </table>
            </td>
          </tr>

          <!-- SECTION 14: PROPERTY ADDRESS -->
          <tr>
            <td align="center" bgcolor="#414446" style="padding: 0; margin: 0; font-size: 0; line-height: 0; background-color: #414446; background-image: linear-gradient(#414446, #414446);">
              <a href="https://maps.apple.com/?q=1221+2nd+Ave+N+Nashville+TN+37208" target="_blank" style="text-decoration: none; display: block;">
                <img src="{u_prop}"
                     width="600"
                     height="75"
                     alt="1221 2ND AVE N, NASHVILLE, TN 37208"
                     class="fluid"
                     style="width: 100%; max-width: 600px; height: auto; display: block; border: 0;" />
              </a>
            </td>
          </tr>

          <!-- SECTION 15: FOOTER BANNER (Stone/Ivy + Logos + Legal Disclaimer) -->
          <tr>
            <td align="center" style="padding: 0; margin: 0; font-size: 0; line-height: 0;">
              <img src="{u_footer}"
                   width="600"
                   height="193"
                   alt="Fulton Residences Footer &amp; Legal Disclaimers"
                   class="fluid"
                   style="width: 100%; max-width: 600px; height: auto; display: block; border: 0;" />
            </td>
          </tr>

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

# 1. Write root index.html
html_local = generate_html("assets/")
with open(os.path.join(HERE, "index.html"), "w", encoding="utf-8") as f:
    f.write(html_local)
print("Saved index.html (assets/ relative)")

# 2. Write root index-hosted.html
html_hosted = generate_html(hosted_map)
with open(os.path.join(HERE, "index-hosted.html"), "w", encoding="utf-8") as f:
    f.write(html_hosted)
print("Saved index-hosted.html (CDN hosted)")

# 3. Write Deliverable/index.html (images/ relative)
html_deliv_local = generate_html("images/")
with open(os.path.join(DELIV_DIR, "index.html"), "w", encoding="utf-8") as f:
    f.write(html_deliv_local)
print("Saved Deliverable/index.html (images/ relative)")

# 4. Write Deliverable/index-hosted.html
with open(os.path.join(DELIV_DIR, "index-hosted.html"), "w", encoding="utf-8") as f:
    f.write(html_hosted)
print("Saved Deliverable/index-hosted.html")

# 5. Write Deliverable/index-client-cdn.html
html_client_cdn = generate_html(CLIENT_CDN)
with open(os.path.join(DELIV_DIR, "index-client-cdn.html"), "w", encoding="utf-8") as f:
    f.write(html_client_cdn)
print("Saved Deliverable/index-client-cdn.html")

# 6. Write Deliverable/mailchimp-template.html
html_mc = html_hosted
html_mc = html_mc.replace("<title>You're Invited — Step Inside Fulton Residences</title>",
                          "<title>*|MC:SUBJECT|*</title>")
# Add Mailchimp CAN-SPAM compliant footer row below Section 15
mc_footer_row = """          <!-- MAILCHIMP CAN-SPAM COMPLIANT FOOTER -->
          <tr>
            <td align="center" bgcolor="#2A2A2A" style="padding: 24px 20px; background-color: #2A2A2A; font-family: Arial, sans-serif; font-size: 11px; line-height: 16px; color: #CCCCCC; text-align: center;">
              <p style="margin: 0 0 10px 0; color: #CCCCCC;">
                You are receiving this email because you expressed interest in Fulton Residences.<br />
                <a href="*|UNSUB|*" style="color: #FFFFFF; text-decoration: underline;">Unsubscribe</a> &nbsp;|&nbsp;
                <a href="*|UPDATE_PROFILE|*" style="color: #FFFFFF; text-decoration: underline;">Update Preferences</a>
              </p>
              <p style="margin: 0; color: #999999;">
                *|LIST:ADDRESSLINE|*<br />
                &copy; *|CURRENT_YEAR|* *|LIST:COMPANY|*. All rights reserved.
              </p>
            </td>
          </tr>
        </table>"""
html_mc = html_mc.replace("        </table>", mc_footer_row)

with open(os.path.join(DELIV_DIR, "mailchimp-template.html"), "w", encoding="utf-8") as f:
    f.write(html_mc)
print("Saved Deliverable/mailchimp-template.html")

# 7. Package ZIP file
zip_path = os.path.join(HERE, "Fulton-Residences-Project-4559216753-Deliverable.zip")
with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
    for root, dirs, files in os.walk(DELIV_DIR):
        for file in files:
            full_p = os.path.join(root, file)
            rel_p = os.path.relpath(full_p, HERE)
            z.write(full_p, rel_p)

print(f"Deliverable package re-zipped: {os.path.getsize(zip_path)//1024} KB")
