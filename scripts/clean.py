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
    if not os.path.exists("/tmp/ids"):
        print("Directory not found, TXT records assumed to be cleaned.")
        exit()
    files = os.listdir("/tmp/ids")
    if len(files) == 0:
         print("Empty directory, TXT records assumed to be cleaned.")
         exit()
    id = files[0]
    r = requests.delete("https://api.cloudflare.com/client/v4/zones/" + zone + "/dns_records/" + id, headers=headers)
    if (not r.status_code in range(200, 299)):
        print("Error " + str(r.status_code))
        print(r.json())
        exit()
    os.remove(f"/tmp/ids/{id}")
    if len(os.listdir("/tmp/ids")) == 0:
         os.rmdir("/tmp/ids")


if __name__ == "__main__":
	main()
