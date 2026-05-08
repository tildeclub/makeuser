#!/usr/bin/python3.8
# Script created/contributed by ~jmjl

import json
import socket
import ssl
import sys
import time


CONFIG_FILE = "/root/.znc-conf/znc-config.json"


def error_exit(message):
    print(f"{sys.argv[0]}: {message}", file=sys.stderr)
    sys.exit(1)


def usage():
    print(
        "usage:\n"
        f"  {sys.argv[0]} <username> <password> [Key=Value ...]\n"
        f"  {sys.argv[0]} <username> --password-stdin [Key=Value ...]",
        file=sys.stderr,
    )


def loadconf(cfgfile):
    with open(cfgfile, "r") as f:
        return json.load(f)


def read_password_from_stdin():
    password = sys.stdin.readline()

    if password == "":
        error_exit("no password received on stdin")

    password = password.rstrip("\r\n")

    if password == "":
        error_exit("empty password received on stdin")

    return password


def parse_args(argv):
    if len(argv) < 3:
        usage()
        error_exit("not enough arguments")

    user = argv[1]

    if not user:
        error_exit("username cannot be empty")

    if argv[2] == "--password-stdin":
        password = read_password_from_stdin()
        settings_args = argv[3:]
    else:
        password = argv[2]
        settings_args = argv[3:]

    if not password:
        error_exit("password cannot be empty")

    cli_settings = {}

    # Parse optional key=value settings after username/password.
    # Example:
    #   MaxNetworks=3 MaxClients=5
    for arg in settings_args:
        if "=" in arg:
            key, value = arg.split("=", 1)
            key = key.strip()
            value = value.strip()

            if key:
                cli_settings[key] = value

    return user, password, cli_settings


def send(sock, msg):
    sock.send(f"{msg}\n".encode("utf-8"))


def main():
    user, pswd, cli_settings = parse_args(sys.argv)

    cfg = loadconf(CONFIG_FILE)

    # Also allow defaults from config, but CLI wins.
    # In /root/.znc-conf/znc-config.json you may add:
    # {
    #   ...,
    #   "default_user_settings": {
    #     "MaxNetworks": "3"
    #   }
    # }
    default_settings = cfg.get("default_user_settings", {}) or {}

    readbuffer = ""

    sock = socket.socket()

    if cfg.get("tls") == "yes":
        ctx = ssl.create_default_context(purpose=ssl.Purpose.CLIENT_AUTH)
        sock = ctx.wrap_socket(sock)

    sock.connect((cfg["srv"], int(cfg["port"])))

    send(sock, "NICK bot")
    send(sock, "USER bot 0 * :A bot to make users")

    while True:
        readbuffer += sock.recv(2048).decode("utf-8", errors="ignore")
        temp = str.split(readbuffer, "\n")
        readbuffer = temp.pop()

        for line in temp:
            line = line.rstrip("\r")
            parts = line.split()

            if len(parts) < 2:
                continue

            # Authenticate when ZNC asks for PASS (ERR_PASSWDMISMATCH 464).
            if parts[1] == "464":
                send(sock, f"PASS {cfg['user']}:{cfg['password']}")

            # On welcome (001), create user and apply settings.
            # Preserves your original hostname check.
            if parts[0][1:] == "irc.znc.in" and parts[1] == "001":
                # Create user.
                send(sock, f"PRIVMSG *controlpanel :AddUser {user} {pswd}")

                # Merge defaults + CLI, CLI overrides.
                effective = dict(default_settings)
                effective.update(cli_settings)

                # Apply settings like:
                #   set MaxNetworks <user> <val>
                for key, val in effective.items():
                    send(sock, f"PRIVMSG *controlpanel :set {key} {user} {val}")

                print(f"Maken znc user {user}")
                sys.exit(0)


if __name__ == "__main__":
    main()
