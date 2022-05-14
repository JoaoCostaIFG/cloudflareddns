#!/usr/bin/env python3

import CloudFlare
import json
import requests

# Uses an external internet page to retrieve the machine's IP address
def getMachineIP(isIPv4=True):
    url = ("https://1.1.1.1" if isIPv4 else "https://[2606:4700:4700::1111]") + "/cdn-cgi/trace"
    try:
        req = requests.get(url).text.split("\n");
        req.pop() # remove last entry (it's empty)
        traceInfo = dict(entry.split("=") for entry in req)
        return traceInfo["ip"]
    except Exception:
        print(f"Failure getting the Machine's IP{'v4' if isIPv4 else 'v6'} address.")
        return None

def main():
    #config = json.loads(config_file.read())

    cf = CloudFlare.CloudFlare()
    getMachineIP(isIPv4=False)

if __name__ == "__main__":
    main()
