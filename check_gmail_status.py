import imaplib

mail = imaplib.IMAP4_SSL("imap.gmail.com", 993)
mail.login("gravityahmed11@gmail.com", "pmvnfpqnkwxpsgwg")
print("IMAP login success!")

# Select '[Gmail]/Sent Mail'
status, count = mail.select('"[Gmail]/Sent Mail"')
print("Sent mail count:", count)

# Check last 3 messages in Sent Mail
status, data = mail.search(None, "ALL")
ids = data[0].split()
print("Total sent ids:", len(ids))
for msg_id in ids[-4:]:
    status, msg_data = mail.fetch(msg_id, "(BODY[HEADER.FIELDS (SUBJECT TO DATE)])")
    print("--- SENT ---")
    print(msg_data[0][1].decode())

# Also check INBOX for any bounce / delivery failure
status, count = mail.select("INBOX")
print("\nInbox count:", count)
status, data = mail.search(None, "ALL")
inbox_ids = data[0].split()
print("Inbox total ids:", len(inbox_ids))
for msg_id in inbox_ids[-4:]:
    status, msg_data = mail.fetch(msg_id, "(BODY[HEADER.FIELDS (FROM SUBJECT DATE)])")
    print("--- INBOX ---")
    print(msg_data[0][1].decode())

mail.logout()
