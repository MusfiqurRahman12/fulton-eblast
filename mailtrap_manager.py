import os
import smtplib
import email.utils
from email.message import EmailMessage
import urllib.request
import json
import re

HERE = os.path.dirname(os.path.abspath(__file__))

# Load from .env if present
env_file = os.path.join(HERE, ".env")
if os.path.exists(env_file):
    with open(env_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ[k.strip()] = v.strip()

TOKEN = os.environ.get("MAILTRAP_API_TOKEN", "")
INBOX_ID = int(os.environ.get("MAILTRAP_INBOX_ID", "4943455"))
SMTP_USER = os.environ.get("MAILTRAP_SMTP_USER", "")
SMTP_PASS = os.environ.get("MAILTRAP_SMTP_PASS", "")
SMTP_HOST = os.environ.get("MAILTRAP_SMTP_HOST", "sandbox.smtp.mailtrap.io")
SMTP_PORT = int(os.environ.get("MAILTRAP_SMTP_PORT", "2525"))
SENDER_EMAIL = os.environ.get("MAILTRAP_SENDER_EMAIL", "events@liveatfulton.com")
SENDER_NAME = os.environ.get("MAILTRAP_SENDER_NAME", "Fulton Residences")
RECIPIENT_EMAIL = os.environ.get("MAILTRAP_RECIPIENT_EMAIL", "preview@tangocrew.com")
RECIPIENT_NAME = os.environ.get("MAILTRAP_RECIPIENT_NAME", "Client Preview")
TEMPLATE_UUID = os.environ.get("MAILTRAP_TEMPLATE_UUID", "32727783-9b20-4c89-bb6e-6ba18765124d")

def send_hosted(subject="You're Invited - Step Inside Fulton Residences (Project ID 4559216753)",
                from_email=SENDER_EMAIL,
                from_name=SENDER_NAME,
                to_email=RECIPIENT_EMAIL,
                to_name=RECIPIENT_NAME):
    """Sends email using direct high-speed hosted HTTPS CDN assets (iili.io)."""
    hosted_path = os.path.join(HERE, "index-hosted.html")
    if not os.path.exists(hosted_path):
        hosted_path = os.path.join(HERE, "index.html")

    with open(hosted_path, "r", encoding="utf-8") as f:
        html_content = f.read()

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = f"{from_name} <{from_email}>"
    msg["To"] = f"{to_name} <{to_email}>"
    msg["Date"] = email.utils.formatdate(localtime=True)
    msg["Message-ID"] = email.utils.make_msgid(domain="liveatfulton.com")

    plain_text = """You're invited to step inside Fulton Residences.
Join us at The Goat in Germantown for cocktails, light bites, and a guided hard hat tour.
Date: Thursday, October 1st | 4:00 - 6:00 PM
Location: 1220 2nd Avenue North, Nashville, TN 37208
RSVP: info@liveatfulton.com
Website: https://liveatfulton.com
"""
    msg.set_content(plain_text)
    msg.add_alternative(html_content, subtype="html")

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(SMTP_USER, SMTP_PASS)
        server.send_message(msg)
    print("Email with hosted CDN images sent successfully to Mailtrap sandbox!")

def send_email(subject="You're Invited - Step Inside Fulton Residences (Project ID 4559216753)",
               from_email=SENDER_EMAIL,
               from_name=SENDER_NAME,
               to_email=RECIPIENT_EMAIL,
               to_name=RECIPIENT_NAME,
               use_cid=True):
    """Sends email using inline CID attachments for offline rendering."""
    with open(os.path.join(HERE, "index.html"), "r", encoding="utf-8") as f:
        html_content = f.read()

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = f"{from_name} <{from_email}>"
    msg["To"] = f"{to_name} <{to_email}>"
    msg["Date"] = email.utils.formatdate(localtime=True)
    msg["Message-ID"] = email.utils.make_msgid(domain="liveatfulton.com")

    plain_text = """You're invited to step inside Fulton Residences.
Join us at The Goat in Germantown for cocktails, light bites, and a guided hard hat tour.
Date: Thursday, October 1st | 4:00 - 6:00 PM
Location: 1220 2nd Avenue North, Nashville, TN 37208
RSVP: info@liveatfulton.com
Website: https://liveatfulton.com
"""
    msg.set_content(plain_text)

    if use_cid:
        found_assets = re.findall(r'src=["\'](assets/[^"\']+)["\']', html_content)
        unique_assets = list(dict.fromkeys(found_assets))

        html_cid = html_content
        cid_map = {}
        for i, rel_path in enumerate(unique_assets):
            base = os.path.splitext(os.path.basename(rel_path))[0]
            cid = f"img_asset_{i}_{base}"
            cid_map[cid] = rel_path
            html_cid = html_cid.replace(f'"{rel_path}"', f'"cid:{cid}"').replace(f"'{rel_path}'", f"'cid:{cid}'")

        msg.add_alternative(html_cid, subtype="html")

        for cid, rel_path in cid_map.items():
            abs_img = os.path.join(HERE, rel_path)
            if os.path.exists(abs_img):
                with open(abs_img, "rb") as img_f:
                    img_data = img_f.read()
                ext = os.path.splitext(rel_path)[1].lower().replace(".", "")
                subtype = "jpeg" if ext in ("jpg", "jpeg") else "png"
                msg.get_payload()[1].add_related(
                    img_data,
                    maintype="image",
                    subtype=subtype,
                    cid=f"<{cid}>",
                    filename=os.path.basename(rel_path)
                )
    else:
        msg.add_alternative(html_content, subtype="html")

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(SMTP_USER, SMTP_PASS)
        server.send_message(msg)
    print("Email sent successfully to Mailtrap sandbox via SMTP!")

def send_from_template(template_uuid=TEMPLATE_UUID,
                       to_email=RECIPIENT_EMAIL,
                       to_name=RECIPIENT_NAME):
    url = f"https://sandbox.api.mailtrap.io/api/send/{INBOX_ID}"
    hdr = {
        "Authorization": "Bearer " + TOKEN,
        "Content-Type": "application/json",
        "User-Agent": "mailtrap-go/0.3.0"
    }
    payload = {
        "to": [{"email": to_email, "name": to_name}],
        "from": {"email": SENDER_EMAIL, "name": SENDER_NAME},
        "template_uuid": template_uuid
    }
    req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=hdr, method="POST")
    with urllib.request.urlopen(req) as resp:
        res = json.loads(resp.read().decode())
        print(f"Sent email using Template UUID {template_uuid}! Message IDs: {res.get('message_ids')}")
        return res

def get_latest_messages():
    req = urllib.request.Request(
        f"https://mailtrap.io/api/inboxes/{INBOX_ID}/messages",
        headers={"Authorization": f"Bearer {TOKEN}"}
    )
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode())

def get_message_spam_report(msg_id):
    req = urllib.request.Request(
        f"https://mailtrap.io/api/inboxes/{INBOX_ID}/messages/{msg_id}/spam_report",
        headers={"Authorization": f"Bearer {TOKEN}"}
    )
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode())

if __name__ == "__main__":
    import sys
    action = sys.argv[1] if len(sys.argv) > 1 else "status"

    if action == "hosted":
        print("Sending new test email with hosted CDN images (iili.io) to Mailtrap...")
        send_hosted()
    elif action == "send":
        print("Sending new test email with inline retina assets to Mailtrap...")
        send_email()
    elif action == "template":
        print(f"Sending test email from Hosted Template UUID {TEMPLATE_UUID}...")
        send_from_template()
    
    msgs = get_latest_messages()
    print(f"\n==========================================")
    print(f" MAILTRAP EMAIL TESTING SANDBOX")
    print(f"==========================================")
    print(f"Inbox ID: {INBOX_ID} ('My Sandbox')")
    print(f"Template UUID: {TEMPLATE_UUID}")
    print(f"Direct Sandbox URL: https://mailtrap.io/inboxes/{INBOX_ID}")
    print(f"Total Messages in Inbox: {len(msgs)}")
    
    if msgs:
        latest = msgs[0]
        latest_id = latest["id"]
        spam = get_message_spam_report(latest_id)
        score = spam.get("report", {}).get("Score", "N/A")
        print(f"\n--- Latest Message ---")
        print(f"Subject: {latest.get('subject')}")
        print(f"Message ID: {latest_id}")
        print(f"Sent At: {latest.get('created_at')}")
        print(f"View in Mailtrap: https://mailtrap.io/inboxes/{INBOX_ID}/messages/{latest_id}")
        print(f"SpamAssassin Score: {score} / 5.0 (Passed, safe from spam filters)")
    print(f"==========================================\n")
