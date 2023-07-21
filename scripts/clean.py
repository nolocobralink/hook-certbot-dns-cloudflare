#!/usr/bin/env python

import os
import requests

def main():
    zone = os.getenv("CERTBOT_ZONE_ID")
    authentication = os.getenv("CERTBOT_BEARER_TOKEN")
    api_key = os.getenv("CERTBOT_API_KEY")
    email = os.getenv("CERTBOT_EMAIL")
    headers = {
        "X-Auth-Email": email, 
        "X-Auth-Key": api_key
    }
    if authentication:
        headers["Authentication"] = "Bearer " + authentication
    if not os.path.isfile("/tmp/ids"):
        print("File not found, TXT records assumed to be cleaned.")
        exit()
    file = open("/tmp/ids", "r")
    ids = file.read().splitlines()
    for id in ids:
        r = requests.delete("https://api.cloudflare.com/client/v4/zones/" + zone + "/dns_records/" + id, headers=headers)
        if (not r.status_code in range(200, 299)):
            print("Error " + str(r.status_code))
            print(r.json())
            exit()
    os.remove("/tmp/ids")


if __name__ == "__main__":
	main()
