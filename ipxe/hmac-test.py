import time, hmac, hashlib, base64, requests

with open("master.key") as f:
    SECRET  = bytes.fromhex(f.read().strip())
machine_id = "my-client-123"

timestamp = str(int(time.time()))

msg = timestamp + machine_id
sig = base64.b64encode(hmac.new(SECRET, msg.encode(), hashlib.sha256).digest()).decode()

headers = {
    "X-Timestamp": timestamp,
    "X-Machine-ID": machine_id,
    "X-Signature": sig
}

r = requests.get("https://83.228.213.33", headers=headers, verify='lamphost-pxe-server-zertifikatskette.pem')
print(r.status_code, r.text)

