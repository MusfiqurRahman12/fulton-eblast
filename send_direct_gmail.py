import os
import sys
import smtplib
import ssl
from email.message import EmailMessage

HERE = os.path.dirname(os.path.abspath(__file__))

# Load .env
env_file = os.path.join(HERE, ".env")
if os.path.exists(env_file):
    with open(env_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ[k.strip()] = v.strip()

SMTP_USER = os.environ.get("GMAIL_USER", "gravityahmed11@gmail.com")
APP_PASS = os.environ.get("GMAIL_APP_PASS", "pmvnfpqnkwxpsgwg")
TO_EMAIL = sys.argv[1] if len(sys.argv) > 1 else os.environ.get("GMAIL_TARGET", "musfiqurrahmansqa@gmail.com")

# Load hosted HTML
html_path = os.path.join(HERE, "index-hosted.html")
with open(html_path, "r", encoding="utf-8") as f:
    html_content = f.read()

plain_text = """You're invited to step inside Fulton Residences.
Join us at The Goat in Germantown for cocktails, light bites, and a guided hard hat tour.
Date: Thursday, October 1st | 4:00 - 6:00 PM
Location: 1220 2nd Avenue North, Nashville, TN 37208
RSVP: info@liveatfulton.com
Website: https://liveatfulton.com
"""

from datetime import datetime

ts_str = datetime.now().strftime("%I:%M %p")
msg = EmailMessage()
msg["Subject"] = f"[Update {ts_str}] Fulton Residences — Step Inside (Seamless Zero-Seam Build)"
msg["From"] = f"Fulton Residences <{SMTP_USER}>"
msg["To"] = TO_EMAIL
msg["Reply-To"] = SMTP_USER
msg.set_content(plain_text)
msg.add_alternative(html_content, subtype="html")

print(f"Connecting to smtp.gmail.com:465 via SSL...")
ctx = ssl.create_default_context()
with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=ctx, timeout=30) as server:
    server.ehlo()
    print(f"Authenticating as {SMTP_USER}...")
    server.login(SMTP_USER, APP_PASS)
    print(f"Dispatching eblast to {TO_EMAIL}...")
    server.send_message(msg)

print("\n==================================================")
print("SUCCESS! Fulton Eblast delivered directly to:")
print(f"  Recipient: {TO_EMAIL}")
print("==================================================")
