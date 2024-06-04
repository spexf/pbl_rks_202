#!/bin/bash

sudo apt-get update
sudo apt install socat
sudo cp ./status.py ~
sudo python3 InitService.py


