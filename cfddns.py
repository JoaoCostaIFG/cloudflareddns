#!/usr/bin/env python3

import CloudFlare
import json
import requests
from os import environ
from os.path import exists as fileExists
from sys import exit

def getRemoteDNSRecords(cf, zoneId):
    dnsRecords = []
    for record in cf.zones.dns_records.get(zoneId):
        dnsRecords.append(
            {
                "id": record["id"],
                "name": record["name"],
                "type": record["type"],
                "content": record["content"],
                "proxied": record["proxied"],
                "ttl": record["ttl"],
            }
        )
    return dnsRecords

# Updates the remote record corresponding to record (if any).
def updateRemoteRecord(cf, zoneId, zoneName, remoteRecords, record):
    if len(record["name"]) > 0:
        # subdomain
        fqdn = f"{record['name']}.{zoneName}"
    else:
        # basedomain
        fqdn = zoneName

    for remote in remoteRecords:
        # check if is duplicate
        if not (fqdn == remote["name"] and record["type"] == remote["type"]):
            # not duplicate
            continue

        # copy missing parameters (keep remote ones if not specified)
        if "proxied" not in record:
            record["proxied"] = remote["proxied"]
        if "ttl" not in record:
            record["ttl"] = remote["ttl"]

        # check if it is up-to-date
        if record["content"] != remote["content"] or record["proxied"] != remote["proxied"] or record["ttl"] != remote["ttl"]:
            # remote record is not up-to-date, updating it
            print(f"Updating remote record: {record}")
            cf.zones.dns_records.put(zoneId, remote["id"], data=record)

        return True

    return False

def genRecord(domain, type, ipv4, proxied, ttl):
    record = {"name": domain, "type": type, "content": ipv4}
    if proxied:
        record["proxied"] = proxied
    if ttl:
        record["ttl"] = ttl
    return record

def processZone(cf, zoneInfo, ipv4, ipv6):
    # get zone ID
    if "zone_id" in zoneInfo:
        zoneId = zoneInfo["zone_id"]
        zoneName = cf.zones.get(params={"id": zoneId})[0]["name"]
    elif "zone_name" in zoneInfo:
        zoneName = zoneInfo["zone_name"]
        zoneId = cf.zones.get(params={"name": zoneName})[0]["id"]
    else:
        raise Exception("No zone name/id given...")

    # get remote DNS records (to find duplicates)
    remoteRecords = getRemoteDNSRecords(cf, zoneId)

    proxied = zoneInfo["proxied"] if "proxied" in zoneInfo else None # defailt is False
    ttl = zoneInfo["ttl"] if "ttl" in zoneInfo else None # default is 1

    dnsRecords = []
    for domain in zoneInfo["subdomains"]:
        if ipv4:
            dnsRecords.append(genRecord(domain, "A", ipv4, proxied, ttl))
        if ipv6:
            dnsRecords.append(genRecord(domain, "AAAA", ipv6, proxied, ttl))

    for record in dnsRecords:
        if updateRemoteRecord(cf, zoneId, zoneName, remoteRecords, record):
            # record had a corresponding remote
            continue
        # this is a new record
        print(f"Creating new remote record: {record}")
        cf.zones.dns_records.post(zoneId, data=record)

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

def getConfigPath():
    if environ.get("CFDDNS_CONFIG"):
        # env var present
        return environ["CFDDNS_CONFIG"]
    elif fileExists("/config.json"):
        return "/config.json"
    return None

def authenticate(authInfo):
    if "api_token" in authInfo:
        return CloudFlare.CloudFlare(token=authInfo["api_token"])
    elif "api_key" in authInfo:
        return CloudFlare.CloudFlare(email=authInfo["api_key"]["email"], token=authInfo["api_key"]["key"])
    # no valid auth info found
    return None

def main():
    configPath = getConfigPath()
    if not configPath:
        print("Config file location not defined. Exiting...")
        exit(1)

    # read config JSON file
    try:
        with open(configPath) as configFile:
            config = json.loads(configFile.read())
    except Exception:
        print(f"Failure reading config file at: {configPath}. Exitting...")
        exit(1)

    # whether or not to use IPv4/IPv6
    doIPv4 = True
    if "IPv4" in config and config["IPv4"] is False:
        doIPv4 = False
    doIPv6 = False
    if "IPv6" in config and config["IPv6"] is True:
        doIPv6 = True

    if doIPv4:
        ipv4 = getMachineIP()
    if doIPv6:
        ipv6 = getMachineIP(isIPv4=False)

    for zone in config["cloudflare"]:
        cf = authenticate(zone["authentication"])
        try:
            processZone(cf, zone, ipv4, ipv6)
        except Exception as e:
            print(f"Caught exception while processing zone: {e}. Continuing...")

if __name__ == "__main__":
    main()
