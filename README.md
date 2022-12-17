# minecraft-server-install

Simple script to help install a vanilla minecraft server in debian/ubuntu systems (**Ubuntu 18.04 LTS** recommended).

To operate the minecraftserver properly as an admin, be sure to know your minecraft UUID and your exact
USERNAME before the install. If you don't know it, then have a look at the usercache.json file after
login in and reinstall the server.

> Versions available from 1.10 to 1.19.3

### Server initial dependencies:

- git
- python3
- systemd

### Cloning and Running:

```bash
$ git clone https://github.com/raibtoffoletto/minecraft-server-install.git
$ cd minecraft-server-install
$ python3 minecraft-server-script.py
```

## Acknowledgments

Special thanks for the team over [MCVersions](https://mcversions.net/) to keep a comprehensive and complete list of Minecraft Servers.

## Disclaimer

This script is in no way associated with Mojang or Microsoft. You will need to purchase a legal copy of Minecraft client to enjoy this server.
