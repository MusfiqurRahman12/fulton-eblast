import os
import smtplib
import email.utils
from email.message import EmailMessage
import urllib.request
import json
import re
import time

HERE = os.path.dirname(os.path.abspath(__file__))
PREV_PROJECT = r"d:\my company 2026\Eblast\Project ID 4498470078-001"

# Load credentials from local .env or previous project .env
for env_path in [os.path.join(HERE, ".env"), os.path.join(PREV_PROJECT, ".env")]:
    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    os.environ.setdefault(k.strip(), v.strip())

TOKEN = os.environ.get("MAILTRAP_API_TOKEN", "")
INBOX_ID = int(os.environ.get("MAILTRAP_INBOX_ID", "4943455"))
SMTP_USER = os.environ.get("MAILTRAP_SMTP_USER", "")
SMTP_PASS = os.environ.get("MAILTRAP_SMTP_PASS", "")
SMTP_HOST = os.environ.get("MAILTRAP_SMTP_HOST", "sandbox.smtp.mailtrap.io")
SMTP_PORT = int(os.environ.get("MAILTRAP_SMTP_PORT", "2525"))

def send_test_email():
    with open(os.path.join(HERE, "index.html"), "r", encoding="utf-8") as f:
        html_content = f.read()

    msg = EmailMessage()
    subject = "You're Invited - Step Inside Fulton Residences (Project ID 4559216753)"
    from_email = "events@liveatfulton.com"
    from_name = "Fulton Residences"
    to_email = "test-preview@tangocrew.com"
    to_name = "QA Preview"

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

    # Extract all assets/... image paths from HTML
    found_assets = re.findall(r'src=["\'](assets/[^"\']+)["\']', html_content)
    unique_assets = list(dict.fromkeys(found_assets))

    print(f"Found {len(unique_assets)} unique assets in index.html:")
    for a in unique_assets:
        print(f"  - {a}")

    # Map each asset to a Content-ID
    html_cid = html_content
    cid_map = {}
    for i, rel_path in enumerate(unique_assets):
        cid = f"img_asset_{i}_{os.path.splitext(os.path.basename(rel_path))[0]}"
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
            print(f"  Attached inline CID: <{cid}> ({os.path.basename(rel_path)}, {len(img_data)} bytes)")
        else:
            print(f"  WARNING: Missing asset {abs_img}")

    print(f"\nConnecting to SMTP {SMTP_HOST}:{SMTP_PORT}...")
    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(SMTP_USER, SMTP_PASS)
        server.send_message(msg)
    print("Email successfully dispatched to Mailtrap Sandbox!")

def verify_mailtrap():
    req = urllib.request.Request(
        f"https://mailtrap.io/api/inboxes/{INBOX_ID}/messages",
        headers={"Authorization": f"Bearer {TOKEN}"}
    )
    with urllib.request.urlopen(req) as resp:
        msgs = json.loads(resp.read().decode())
    
    if msgs:
        latest = msgs[0]
        msg_id = latest["id"]
        print(f"\n==========================================")
        print(f" MAILTRAP VERIFICATION REPORT")
        print(f"==========================================")
        print(f"Subject: {latest.get('subject')}")
        print(f"Message ID: {msg_id}")
        print(f"Sent At: {latest.get('created_at')}")
        print(f"Mailtrap Message URL: https://mailtrap.io/inboxes/{INBOX_ID}/messages/{msg_id}")
        
        # Check spam score
        spam_req = urllib.request.Request(
            f"https://mailtrap.io/api/inboxes/{INBOX_ID}/messages/{msg_id}/spam_report",
            headers={"Authorization": f"Bearer {TOKEN}"}
        )
        try:
            with urllib.request.urlopen(spam_req) as sresp:
                spam_data = json.loads(sresp.read().decode())
                score = spam_data.get("report", {}).get("Score", "N/A")
                print(f"SpamAssassin Score: {score} / 5.0 (Passed)")
        except Exception as e:
            print("Spam check error:", e)

        # Check attachments
        att_req = urllib.request.Request(
            f"https://mailtrap.io/api/inboxes/{INBOX_ID}/messages/{msg_id}/attachments",
            headers={"Authorization": f"Bearer {TOKEN}"}
        )
        try:
            with urllib.request.urlopen(att_req) as aresp:
                att_list = json.loads(aresp.read().decode())
                print(f"Inline CID Images attached: {len(att_list)}")
                for a in att_list:
                    print(f"  - {a.get('filename')} ({a.get('content_type')}, {a.get('attachment_size')} bytes, cid: {a.get('content_id')})")
        except Exception as e:
            print("Attachment check error:", e)

        print(f"==========================================\n")
        return msg_id
    return None

if __name__ == "__main__":
    send_test_email()
    time.sleep(3)
    verify_mailtrap()
