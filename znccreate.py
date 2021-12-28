#!/usr/bin/python3.8
import socket, ssl, json, time, sys
# Takes the first argument as a username and the second as the password.
def loadconf(cfgfile):
    with open(cfgfile, 'r') as f:
        cfg = json.load(f)
    return cfg
def send(msg):
    s.send(f"{msg}\n".encode('utf-8'))

cfg = loadconf("znc-config.json")

readbuffer=""
s = socket.socket()
if cfg['tls'] == 'yes':
    ctx = ssl.create_default_context(purpose=ssl.Purpose.CLIENT_AUTH)
    s = ctx.wrap_socket(s)
s.connect((cfg['srv'], int(cfg['port'])))
send("NICK bot")
send("USER bot 0 * :A bot to make users")

while True:
    readbuffer = readbuffer + s.recv(2048).decode('utf-8')
    temp = str.split(readbuffer, "\n")
    readbuffer = temp.pop()

    for line in temp:
        line = str.rstrip(line)
        line = str.split(line)

        #print(' '.join(line))
        if line[1] == '464':
            send(f"PASS {cfg['user']}:{cfg['password']}")
        if line[0][1:] == 'irc.znc.in' and line[1] == '001':
            user = sys.argv[1]
            pswd = sys.argv[2]
            send(f"PRIVMSG *controlpanel :AddUser {user} {pswd}")
            print(f"Maken znc user {user}")
            sys.exit(0)
