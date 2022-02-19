#!/usr/bin/env python

import os
import requests

def main():
    zona = os.getenv("CERTBOT_ZONE_ID")
    authentication = os.getenv("CERTBOT_BEARER_TOKEN")
    api_key = os.getenv("CERTBOT_API_KEY")
    correo = os.getenv("CERTBOT_EMAIL")
    if not os.path.isfile("/tmp/ids"):
        print("No se encuentra el archivo, se asume que ya se limpiaron los registros TXT.")
        exit()
    archivo = open("/tmp/ids", "r")
    ids = archivo.read().splitlines()
    for id in ids:
        r = requests.delete("https://api.cloudflare.com/client/v4/zones/" + zona + "/dns_records/" + id, headers={ "Authentication": "Bearer " + authentication, "X-Auth-Email": correo, "X-Auth-Key": api_key })
        if (not r.status_code in range(200, 299)):
            print("Error " + str(r.status_code))
            print(r.json())
            exit()
    os.remove("/tmp/ids")


if __name__ == "__main__":
	main()
