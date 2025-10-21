import hashlib
import hmac
import base64
import json
import time
import requests

# ⚙️ Replace with your Sandbox credentials
access_key = "rak_12A02B08FAF6B4C026C0"
secret_key = "rsk_f4ba780e1081da86b4dec9e9ab72e24a98d877f023b58c57f158d9485cd07f90fe7f72c352757670"

base_url = "https://sandboxapi.rapyd.net"

def generate_signature(method, url_path, body):
    salt = str(int(time.time() * 1000))
    timestamp = str(int(time.time()))
    
    # ✅ Ensure body is serialized without spaces
    body_str = "" if body is None else json.dumps(body, separators=(',', ':'), ensure_ascii=False)

    # ✅ Concatenate in the exact order required by Rapyd
    to_sign = f"{method.lower()}{url_path}{salt}{timestamp}{access_key}{secret_key}{body_str}"

    h = hmac.new(secret_key.encode('utf-8'), to_sign.encode('utf-8'), hashlib.sha256)
    signature = base64.b64encode(h.digest()).decode('utf-8')

    return {
        "signature": signature,
        "salt": salt,
        "timestamp": timestamp
    }

def make_request(method, endpoint, body=None):
    url_path = f"/v1/{endpoint}"
    sig = generate_signature(method, url_path, body)

    headers = {
        "Content-Type": "application/json",
        "access_key": access_key,
        "salt": sig["salt"],
        "timestamp": sig["timestamp"],
        "signature": sig["signature"]
    }

    response = requests.request(method, base_url + url_path, headers=headers, json=body)
    return response.json()

# ✅ Important: Wrap numeric values as strings
payment_body = {
    "amount": "100",  # must be string
    "currency": "USD",
    "payment_method": {
        "type": "us_visa_card",
        "fields": {
            "number": "4111111111111111",
            "expiration_month": "12",
            "expiration_year": "25",
            "cvv": "123",
            "name": "John Doe"
        }
    },
    "capture": True
}

result = make_request("post", "payments", payment_body)
print(json.dumps(result, indent=2))
