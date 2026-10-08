import urllib.request
import os

url = "https://catbox.moe/user/api.php"
filepath = "assets/top-bar-2x.jpg"

boundary = "----WebKitFormBoundaryCatbox123"
with open(filepath, "rb") as f:
    img_bytes = f.read()

parts = [
    f"--{boundary}".encode("utf-8"),
    b'Content-Disposition: form-data; name="reqtype"',
    b"",
    b"fileupload",
    f"--{boundary}".encode("utf-8"),
    b'Content-Disposition: form-data; name="fileToUpload"; filename="top-bar-2x.jpg"',
    b"Content-Type: image/jpeg",
    b"",
    img_bytes,
    f"--{boundary}--".encode("utf-8"),
    b""
]
body = b"\r\n".join(parts)

req = urllib.request.Request(
    url,
    data=body,
    headers={
        "Content-Type": f"multipart/form-data; boundary={boundary}",
        "User-Agent": "Mozilla/5.0"
    }
)

with urllib.request.urlopen(req) as resp:
    res = resp.read().decode("utf-8").strip()
    print("CATBOX RESULT:", res)
