import urllib.request
import urllib.parse
import json
import base64
import os

API_KEY = "6d207e02198a847aa98d0a2a901485a5"
UPLOAD_URL = "https://freeimage.host/api/1/upload"

filepath = "assets/top-bar-2x.jpg"

boundary = "----WebKitFormBoundary7MA4YWxkTrZu0gW"
with open(filepath, "rb") as f:
    img_bytes = f.read()

parts = [
    f"--{boundary}".encode("utf-8"),
    b'Content-Disposition: form-data; name="key"',
    b"",
    API_KEY.encode("utf-8"),
    f"--{boundary}".encode("utf-8"),
    b'Content-Disposition: form-data; name="action"',
    b"",
    b"upload",
    f"--{boundary}".encode("utf-8"),
    b'Content-Disposition: form-data; name="source"; filename="top-bar-2x.jpg"',
    b"Content-Type: image/jpeg",
    b"",
    img_bytes,
    f"--{boundary}--".encode("utf-8"),
    b""
]
body = b"\r\n".join(parts)

req = urllib.request.Request(
    UPLOAD_URL,
    data=body,
    headers={
        "Content-Type": f"multipart/form-data; boundary={boundary}",
        "User-Agent": "Mozilla/5.0"
    }
)

try:
    with urllib.request.urlopen(req) as resp:
        res = json.loads(resp.read().decode("utf-8"))
        print("UPLOAD SUCCESS:", res["image"]["url"])
except urllib.error.HTTPError as e:
    print("HTTP Error:", e.code, e.read().decode())
