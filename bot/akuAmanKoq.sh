#!/bin/bash

sudo apt-get update
sudo apt install socat -y
sudo apt install python3-pip -y
sudo pip install scapy
sudo cp ./status.py ~
sudo python3 InitService.py


