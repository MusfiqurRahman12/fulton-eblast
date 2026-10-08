import urllib.request
import os
import json

url = 'https://catbox.moe/user/api.php'
files = [
    'body-copy-2x.jpg',
    'event-details-2x.jpg',
    'rsvp-btn-2x.jpg',
    'space-limited-2x.jpg',
    'reservations-copy-2x.jpg',
    'schedule-btn-2x.jpg',
    'divider-2x.jpg',
    'explore-cta-2x.jpg',
    'property-address-2x.jpg',
    'goat-logo-banner-2x.jpg'
]

import time

# Check already uploaded
if os.path.exists('catbox_sliced_urls.json'):
    try:
        with open('catbox_sliced_urls.json', 'r') as f:
            uploaded = json.load(f)
    except Exception:
        uploaded = {}
else:
    uploaded = {}

for fname in files:
    if fname in uploaded:
        print(f"Skipping already uploaded: {fname} -> {uploaded[fname]}")
        continue
    fpath = os.path.join('assets', fname)
    boundary = '----WebKitFormBoundaryCatbox123'
    with open(fpath, 'rb') as f:
        img_bytes = f.read()

    parts = [
        f'--{boundary}'.encode('utf-8'),
        b'Content-Disposition: form-data; name="reqtype"',
        b'',
        b'fileupload',
        f'--{boundary}'.encode('utf-8'),
        f'Content-Disposition: form-data; name="fileToUpload"; filename="{fname}"'.encode('utf-8'),
        b'Content-Type: image/jpeg',
        b'',
        img_bytes,
        f'--{boundary}--'.encode('utf-8'),
        b''
    ]
    body = b'\r\n'.join(parts)

    success = False
    for attempt in range(4):
        try:
            req = urllib.request.Request(
                url,
                data=body,
                headers={
                    'Content-Type': f'multipart/form-data; boundary={boundary}',
                    'User-Agent': 'Mozilla/5.0'
                }
            )
            with urllib.request.urlopen(req, timeout=45) as resp:
                res = resp.read().decode('utf-8').strip()
                if res.startswith('http'):
                    print(f'{fname} -> {res}')
                    uploaded[fname] = res
                    success = True
                    with open('catbox_sliced_urls.json', 'w') as f:
                        json.dump(uploaded, f, indent=2)
                    time.sleep(2)
                    break
        except Exception as e:
            print(f'Attempt {attempt+1} failed for {fname}: {e}')
            time.sleep(3)
    if not success:
        print(f'ERROR: Failed to upload {fname}')


with open('catbox_sliced_urls.json', 'w') as f:
    json.dump(uploaded, f, indent=2)
print('Done uploading slices!')
