#!/usr/bin/env python3
# SCRIPT:       heddns
# AUTHOR:       Holger (holger@sohonet.ch)
# DATE:         20200624
# REVISION:     1.0
# PLATFORM:     Python
# PURPOSE:      update dynamic DNS entries at Hurricane Electric
# REV. LIST:    DATE            AUTHOR      MODIFICATION
# 1.0           20200624        Holger      - initial script

# TODO
# - everything

# imports:
import requests
import ipaddress
import sys
import dns.resolver


# config-variables:
getPublicIpURL = 'https://icanhazip.com'
fqdn = "your.domain.com"
key = "GENERATEDSECRETKEY"


def setIP(ip):
    setUrl = "https://%s:%s@dyn.dns.he.net/nic/update?hostname=%s&myip=%s" % (fqdn, key, fqdn, ip)
    setResult = requests.get(setUrl)

    if "nochg" in setResult.content.decode('utf-8'):
        print("no need to set. IP already %s for %s" % (ip, fqdn))
    elif "good" in setResult.content.decode('utf-8'):
        print("new IP (%s) set to FQDN (%s)" % (ip, fqdn))
    else:
        print("something went wrong!\nresponse-code: %s\nrepsonse-message: %s" % (setResult.status_code, setResult.content.decode('utf-8')))
        sys.exit(1)


def getIPfromName(searchfqdn):
    dns_resolver = dns.resolver.Resolver()
    dns_resolver.nameservers = ['216.218.130.2', '216.218.131.2', '216.218.132.2', '216.66.1.2', '216.66.80.18']
    result = dns_resolver.query(searchfqdn, 'A')
    for ipval in result:
        return ipval.to_text()


def getPublicIP():
    htmlRequest = requests.get(getPublicIpURL)
    return htmlRequest.content.decode('utf-8').rstrip()


def readPublicIPfromCache():
    cacheFile = open(publicIpCacheFile, "r")
    cachedPIP = cacheFile.read()
    return cachedPIP


def stringToIP(ip):
    try:
        receivedIP = ipaddress.ip_address(ip)
        return receivedIP
    except Exception as Msg:
        print(Msg)
        sys.exit(1)


if __name__ == '__main__':
    _publicIP = stringToIP(getPublicIP())
    _storedIP = stringToIP(getIPfromName(fqdn))

    if _publicIP == _storedIP:
        print("public IP didn't change. nothing to do...")
        sys.exit(0)
    else:
        print("stored public IP: %s\nnew public IP: %s" % (_storedIP, _publicIP))
        setIP(_publicIP)

    print("script finished.")
    sys.exit(0)
