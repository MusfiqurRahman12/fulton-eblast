import json
import urllib.request
import os

HERE = os.path.dirname(os.path.abspath(__file__))

TOKEN = None
for line in open(os.path.join(HERE, ".env"), encoding="utf-8"):
    if line.startswith("MAILTRAP_API_TOKEN="):
        TOKEN = line.split("=", 1)[1].strip()

URL = "https://mailtrap.io/api/accounts/2849014/email_templates/78245"
HDR = {
    "Authorization": "Bearer " + TOKEN,
    "Content-Type": "application/json",
    "User-Agent": "mailtrap-python/1.0"
}

html = open(os.path.join(HERE, "index-hosted.html"), encoding="utf-8").read()

plain_text = """You're invited to step inside Fulton Residences.
Join us at The Goat in Germantown for cocktails, light bites, and a guided hard hat tour.
Date: Thursday, October 1st | 4:00 - 6:00 PM
Location: 1220 2nd Avenue North, Nashville, TN 37208
RSVP: info@liveatfulton.com
Website: https://liveatfulton.com
"""

payload = {
    "email_template": {
        "name": "Fulton - You are Invited Step Inside (Project 4559216753)",
        "category": "Eblast",
        "subject": "You're Invited - Step Inside Fulton Residences (Project ID 4559216753)",
        "body_html": html,
        "body_text": plain_text
    }
}

req = urllib.request.Request(URL, data=json.dumps(payload).encode("utf-8"), headers=HDR, method="PATCH")
with urllib.request.urlopen(req) as resp:
    print(f"Template 78245 Updated with Hosted Images! Status: {resp.status}")

# Send a test email from this updated template
send_url = "https://sandbox.api.mailtrap.io/api/send/4943455"
send_hdr = {
    "Authorization": "Bearer " + TOKEN,
    "Content-Type": "application/json",
    "User-Agent": "mailtrap-go/0.3.0"
}
send_payload = {
    "to": [{"email": "preview@tangocrew.com", "name": "Client Preview"}],
    "from": {"email": "events@liveatfulton.com", "name": "Fulton Residences"},
    "template_uuid": "32727783-9b20-4c89-bb6e-6ba18765124d"
}
send_req = urllib.request.Request(send_url, data=json.dumps(send_payload).encode("utf-8"), headers=send_hdr, method="POST")
with urllib.request.urlopen(send_req) as s_resp:
    res = json.loads(s_resp.read().decode("utf-8"))
    msg_id = res["message_ids"][0]
    print(f"\n==========================================")
    print(f" MAILTRAP EMAIL DISPATCH REPORT")
    print(f"==========================================")
    print(f"Message ID: {msg_id}")
    print(f"Template UUID: 32727783-9b20-4c89-bb6e-6ba18765124d")
    print(f"View in Mailtrap: https://mailtrap.io/inboxes/4943455/messages/{msg_id}")
    print(f"==========================================\n")
