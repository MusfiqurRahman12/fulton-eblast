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
├── index.html                  # Production HTML template (relative "images/" paths)
├── index-hosted.html           # Standalone HTML template (official HTTPS CDN image URLs)
├── index-client-cdn.html       # Official client CDN template (assets.tangocrew.com URLs)
├── mailchimp-template.html     # Mailchimp master template (mc:edit regions + CAN-SPAM merge tags)
├── README.md                   # Technical documentation & ESP deployment guide
├── images/                     # Optimized 2x Retina production assets
│   ├── top-bar-2x.png          # Pricing bar (1200x79, 600x40 display)
│   ├── header-banner-2x.jpg    # Fulton logo + stone/ivy banner (1200x394, 600x197 display)
│   ├── youre-invited-2x.png    # Mauve "You're Invited" serif banner (1200x200, 600x100 display)
│   ├── body-copy-2x.png        # Event invitation copy (1200x923, 600x461 display)
│   ├── goat-logo-2x.png        # The Goat logo centered on #51504F (1200x218, 600x109 display)
│   ├── event-details-2x.png    # Event address + date/time (1200x276, 600x138 display)
│   ├── rsvp-btn-2x.png         # RSVP To Attend CTA button (1200x130, 600x65 display)
│   ├── space-limited-2x.png    # Space is Limited microcopy (1200x110, 600x55 display)
│   ├── interior-photo-2x.jpg   # High-res interior residence photo (1200x730, 600x365 display)
│   ├── reservations-copy-2x.png# Reservations copy (1200x240, 600x120 display)
│   ├── schedule-btn-2x.png     # Schedule A Private Presentation CTA (1200x150, 600x75 display)
│   ├── divider-2x.png          # Mauve divider bar (1200x80, 600x40 display)
│   ├── explore-cta-2x.png      # Explore website CTA (1200x260, 600x130 display)
│   ├── social-fb-2x.png        # Facebook icon on #51504F (600x110, 300x55 display)
│   ├── social-ig-2x.png        # Instagram icon on #51504F (600x110, 300x55 display)
│   ├── property-address-2x.png # Property address (1200x145, 600x72 display)
│   └── footer-banner-2x.jpg    # Footer logos + Equal Housing banner + Legal disclaimer (1200x385, 600x193 display)
└── previews/
    ├── preview-desktop.png     # Full-length 600px desktop render
    └── preview-mobile.png      # Fluid 390px mobile viewport render
```

---

## 🚀 Which Template Should I Use?

| File | Best Used For | Notes |
| :--- | :--- | :--- |
| **`index-hosted.html`** | **Direct Sending & Fast Preview** | Self-contained, single-file HTML. All images load directly from GitHub repository CDN (`https://raw.githubusercontent.com/MusfiqurRahman12/fulton-eblast/main/assets/`). Works immediately in any ESP or CRM (HubSpot, Salesforce, Klaviyo, SendGrid, Mailtrap) without uploading assets. Zero dark-mode color shifting on iPhone Gmail. |
| **`index-client-cdn.html`** | **Official Client CDN Deployment** | Points to official client asset path: `https://assets.tangocrew.com/Fulton/4559216753/`. Deploy after assets are synced to client media server. |
| **`mailchimp-template.html`** | **Mailchimp Campaigns** | Master Mailchimp template including CAN-SPAM compliant unsubscribe/preference merge tags and responsive table layout. |
| **`index.html`** | **Self-Hosted / ZIP Upload** | References `./images/`. Upload the `images/` folder alongside `index.html` to your media server or ZIP-based ESP importer. |

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
