#!/usr/bin/env python3

import sys, re, subprocess

from http.server import HTTPServer, BaseHTTPRequestHandler

if len(sys.argv)-1 != 1:
    print("Usage: {} <port_number>".format(sys.argv[0]))
    sys.exit()

def FindURL(string): 
    # findall() has been used  
    # with valid conditions for urls in string 
    regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    url = re.findall(regex,string)       
    return [x[0] for x in url] 

class Redirect(BaseHTTPRequestHandler):
    def do_GET(self):
        # get code-server logs
        result = subprocess.run(['journalctl', '-u', 'code-server@coder', '-o', 'cat', '--no-pager'], stdout=subprocess.PIPE)
        result = result.stdout.decode('utf-8')

        # try to find the URL
        try:
            urls = FindURL(result)
            url = urls[-1]
        except:
            url = "https://github.com/bpmct/coder-cloud-redirect-server/blob/master/README.md#troubleshooting"
        self.send_response(302)
        self.send_header('Location', url)
        self.end_headers()

print("Starting redirect server on port", sys.argv[1])
HTTPServer(("", int(sys.argv[1])), Redirect).serve_forever()
