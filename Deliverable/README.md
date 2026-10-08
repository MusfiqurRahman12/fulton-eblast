# Fulton Residences: You're Invited — Step Inside
### Project ID: `4559216753` (Germantown, Nashville, TN)
**Due Date:** Thursday, October 8th, 2026

---

## 📦 Deliverable Package Overview

This package contains production-ready, dark-mode hardened HTML email templates, optimized 2x Retina assets, and client preview renders for the **Fulton: You are Invited Step Inside** eblast.

Built using the **Fourteen Park (`Project ID 4498470078-001`)** zero-seam architecture:
* **100% Seamless Full-Width Retina Coverage**: Slices span the full 600px container width (and 300+300 split for social icons) with zero exposed HTML padding cells.
* **Exact Color Harmony (`#51504F`)**: Lossless background color matching across every image slice and outer HTML wrapper table (`RGB: 81, 80, 79`).
* **Bulletproof Dark Mode Protection**: `color-scheme: light only` header directives and vector-rendered image slices prevent iOS Mail, Apple Mail, and Gmail App from inverting or darkening text, buttons, and links.
* **Official Client Enterprise CDN**: All assets are uploaded and live on the client's official FTP media server (`https://assets.tangocrew.com/Fulton/4559216753/`).

```
Deliverable/
├── index.html                  # Production HTML template (Client CDN URLs - ready for deployment)
├── index-hosted.html           # Standalone HTML template (Client CDN URLs)
├── index-client-cdn.html       # Official client CDN template (assets.tangocrew.com URLs)
├── mailchimp-template.html     # Mailchimp master template (mc:edit regions + CAN-SPAM merge tags)
├── README.md                   # Technical documentation & ESP deployment guide
└── previews/
    ├── preview-desktop.png     # Full-length 600px desktop render
    └── preview-mobile.png      # Fluid 390px mobile viewport render
```

---

## 🚀 Which Template Should I Use?

| File | Best Used For | Notes |
| :--- | :--- | :--- |
| **`index.html`** / **`index-client-cdn.html`** | **Production & ESP Deployment** | Production template pointing to official client CDN (`https://assets.tangocrew.com/Fulton/4559216753/`). All assets are live and CDN-hosted with zero local image dependencies. Works immediately in any ESP/CRM (HubSpot, Salesforce, Klaviyo, SendGrid). |
| **`index-hosted.html`** | **Direct Sending & Fast Preview** | Standalone single-file HTML utilizing official HTTPS CDN image URLs. Works immediately with zero dark-mode color shifting on iPhone Gmail. |
| **`mailchimp-template.html`** | **Mailchimp Campaigns** | Master Mailchimp template including `mc:edit` editable sections and CAN-SPAM compliant unsubscribe/preference merge tags. |

---

## 🔗 Production Links & Destination URLs

* **Primary Website**: `https://liveatfulton.com`
* **RSVP Button & Email**: `mailto:info@liveatfulton.com?subject=I%20want%20to%20come%20to%20the%20event`
* **Private Presentation**: `mailto:info@liveatfulton.com?subject=I%20want%20to%20more%20information%20about%20Fulton`
* **Explore Fulton Residences**: `https://liveatfulton.com`
* **The Goat Event Address**: `https://maps.apple.com/?q=1220+2nd+Avenue+North+Nashville+TN+37208`
* **Property Address**: `https://maps.apple.com/?q=1221+2nd+Ave+N+Nashville+TN+37208`
* **Facebook**: `https://www.facebook.com/fultonresidences`
* **Instagram**: `https://www.instagram.com/fultonnashville/`

---

## 🛡️ Fourteen Park Architecture Highlights

* **Zero Seams**: Eliminates all color banding and rectangular boundary boxes by ensuring contiguous edge-to-edge coverage across every block.
* **Zero Dark Mode Inversion**: Live HTML text inversion bugs in iOS Gmail and Android Dark Mode are completely eliminated. All text and buttons stay crisp, bright, and legible.
* **Explore CTA Lock**: The "Explore Fulton Residences" CTA is bold white with underline, matching the PDF specification, and never alters in Light or Dark mode.
* **Retina Clarity**: All slices are 2x (1200px wide) rendered directly from vector PDF sources for crystal clarity on 4K, OLED, and Retina mobile screens.
