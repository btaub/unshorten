#!/usr/bin/env python3

import requests
import urllib3
import argparse
import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
checked = False

# share.google
def share_google(url):
    while True:
        try:
            r = requests.get(url, allow_redirects=False, verify=False)
            if "share.google" in url:
                 url = r.headers['Location']
            else:
                 return(url)
                 break

        except:
           return("something went wrong")
           break

# LinkedIn
def linked_in(url):
    r = requests.get(url)
    for ln in r.text.split('\n'):
        if 'extern' in ln:
            for ln in ln.split('"'):
                if ln.startswith('http'):
                    return(ln)

# Generic location header-based HEAD request
def head_req(url):
    try:
        r = requests.head(url, allow_redirects=False)
        res = r.headers['location']

    except Exception as e:
        print(f"head_req_exception: {e}")
        res = 'head_Err'

    return(res)

# Try get if head fails
def get_req(url):
    try:
        r = requests.get(url, allow_redirects=False, verify=False)
        res = r.headers['location']
    except Exception as e:
        print(f"get_req exception: {e}")
        res = 'get_Err'

    return(res)

def unshorten(url):
    checked = False

    # Reject attempts to hit port numbers. This helps
    # avoid using this as a rudimentary port scanner
    if re.search(r':\d+', url):
        res = "Invalid url, try again"
        checked = True
        return(res)

    # Specify https if missing or if http-only
    if not url.startswith("https://"):
        url = url.replace("http://","")
        url = f"https://{url}"

    # Fix copy-paste errors
    if url.endswith("/"):
         url = url.rstrip("/")

    if 'share.google' in url:
        res = share_google(url)
        checked = True

    # LinkedIn rarely redirects using a Location header, but mostly uses embedded links
    if 'lnkd.in' in url:
        res = head_req(url)
        if not res:
            res = linked_in(url)
        checked = True

    # And the rest of them
    if not checked:
        res = head_req(url)
    if res == 'head_Err':
        res = get_req(url)
    if '.' not in url:
        res = 'Err, no dot'

    return(res)


if __name__ == "__main__":
    # TODO: figure out how to run this with verbosity if it's run as a script
    parser = argparse.ArgumentParser(description="Unshort a short link",
                                      formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("url", help="The URL to check, e.g. https://git.io/h")
    #parser.add_argument("-v", "--verbose",action="store_true",help="Verbose output",default=False)
    args = parser.parse_args()

    print(unshorten(args.url))

