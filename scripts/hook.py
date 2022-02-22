#!/usr/bin/env python

import os
import requests
import time

def main():
    dominio = os.getenv("CERTBOT_DOMAIN")
    zona = os.getenv("CERTBOT_ZONE_ID")
    authentication = os.getenv("CERTBOT_BEARER_TOKEN")
    api_key = os.getenv("CERTBOT_API_KEY")
    correo = os.getenv("CERTBOT_EMAIL")
    contenido = os.getenv("CERTBOT_VALIDATION")
    cuerpo = { 
        "type": "TXT", 
        "name": "_acme-challenge." + dominio, 
        "content": contenido, 
        "ttl": 60 
    }
    headers = {
        "X-Auth-Email": correo, 
        "X-Auth-Key": api_key
    }
    if authentication:
        headers["Authentication"] = "Bearer " + authentication
    r = requests.post("https://api.cloudflare.com/client/v4/zones/" + zona + "/dns_records", json=cuerpo, headers=headers)
    if (not r.status_code in range(200, 299)):
        print("Error " + str(r.status_code))
        print(r.json())
        exit()
    id = r.json()["result"]["id"]
    nueva_linea = os.path.isfile("/tmp/ids")
    archivo = open("/tmp/ids", "a+")
    if nueva_linea:
        archivo.write("\n")
    archivo.write(id)
    time.sleep(60)


if __name__ == "__main__":
	main()
