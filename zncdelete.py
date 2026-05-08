#!/usr/bin/python3.8
# Script created/contributed by ~jmjl

import socket
import ssl
import json
import sys


def loadconf(cfgfile):
    with open(cfgfile, 'r') as f:
        return json.load(f)


def send(msg):
    s.send(f"{msg}\n".encode('utf-8'))


cfg = loadconf("/root/.znc-conf/znc-config.json")

readbuffer = ""
s = socket.socket()
if cfg.get('tls') == 'yes':
    ctx = ssl.create_default_context(purpose=ssl.Purpose.CLIENT_AUTH)
    s = ctx.wrap_socket(s)

s.connect((cfg['srv'], int(cfg['port'])))
send("NICK bot")
send("USER bot 0 * :A bot to remove users")

if len(sys.argv) != 2:
    print("usage: zncdelete.py <username>")
    sys.exit(1)

user = sys.argv[1]

while True:
    readbuffer += s.recv(2048).decode('utf-8', errors='ignore')
    temp = str.split(readbuffer, "\n")
    readbuffer = temp.pop()

    for line in temp:
        line = line.rstrip("\r")
        parts = line.split()

        if len(parts) < 2:
            continue

        if parts[1] == '464':
            send(f"PASS {cfg['user']}:{cfg['password']}")

        if parts[0][1:] == 'irc.znc.in' and parts[1] == '001':
            send(f"PRIVMSG *controlpanel :DelUser {user}")
            print(f"Removed znc user {user}")
            sys.exit(0)
