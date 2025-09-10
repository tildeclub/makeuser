#!/usr/bin/python3.8
# Script created/contributed by ~jmjl

import socket, ssl, json, time, sys

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
send("USER bot 0 * :A bot to make users")

# Parse optional key=value settings after username/password.
# Example: MaxNetworks=3 MaxClients=5
cli_settings = {}
for arg in sys.argv[3:]:
    if '=' in arg:
        k, v = arg.split('=', 1)
        k = k.strip()
        v = v.strip()
        if k:
            cli_settings[k] = v

# Also allow defaults from config, but CLI wins.
# In /root/.znc-conf/znc-config.json you may add:
# { ..., "default_user_settings": { "MaxNetworks": "3" } }
default_settings = cfg.get("default_user_settings", {}) or {}

while True:
    readbuffer += s.recv(2048).decode('utf-8', errors='ignore')
    temp = str.split(readbuffer, "\n")
    readbuffer = temp.pop()

    for line in temp:
        line = line.rstrip("\r")
        parts = line.split()

        if len(parts) < 2:
            continue

        # Authenticate when ZNC asks for PASS (ERR_PASSWDMISMATCH 464).
        if parts[1] == '464':
            send(f"PASS {cfg['user']}:{cfg['password']}")

        # On welcome (001), create user and apply settings.
        # (Preserves your original hostname check.)
        if parts[0][1:] == 'irc.znc.in' and parts[1] == '001':
            user = sys.argv[1]
            pswd = sys.argv[2]

            # Create user (unchanged)
            send(f"PRIVMSG *controlpanel :AddUser {user} {pswd}")

            # Merge defaults + CLI, CLI overrides
            effective = dict(default_settings)
            effective.update(cli_settings)

            # Apply settings like: set MaxNetworks <user> <val>
            for key, val in effective.items():
                send(f"PRIVMSG *controlpanel :set {key} {user} {val}")

            print(f"Maken znc user {user}")
            sys.exit(0)
