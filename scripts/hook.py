#!/usr/bin/env python

import os
import requests
import time

def main():
    if not os.path.exists("/tmp/ids"):
         os.mkdir("/tmp/ids")
    domain = os.getenv("CERTBOT_DOMAIN")
    zone = os.getenv("CERTBOT_ZONE_ID")
    authentication = os.getenv("CERTBOT_BEARER_TOKEN")
    api_key = os.getenv("CERTBOT_API_KEY")
    email = os.getenv("CERTBOT_EMAIL")
    content = os.getenv("CERTBOT_VALIDATION")
    body = { 
        "type": "TXT", 
        "name": "_acme-challenge." + domain, 
        "content": content, 
        "ttl": 60 
    }
    headers = {
        "X-Auth-Email": email, 
        "X-Auth-Key": api_key
    }
    if authentication:
        headers["Authentication"] = "Bearer " + authentication
    r = requests.post("https://api.cloudflare.com/client/v4/zones/" + zone + "/dns_records", json=body, headers=headers)
    if (not r.status_code in range(200, 299)):
        print("Error " + str(r.status_code))
        print(r.json())
        exit()
    id = r.json()["result"]["id"]
    archivo = open(f"/tmp/ids/{id}", "w")
    archivo.close()
    time.sleep(60)


if __name__ == "__main__":
	main()
