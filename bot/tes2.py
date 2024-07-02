import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(4)
print(s.connect(('192.168.109.145', 80)))
s.send_header("Accept-language", "en-US,en,q=0.5")
print(s)
