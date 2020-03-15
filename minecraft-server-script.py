#!/usr/bin/env python3

#####################################################################
#                                                                   #
# Copyright (c) 2019 Raí B. Toffoletto (https://toffoletto.me)      #
#                                                                   #
# This program is free software; you can redistribute it and/or     #
# modify it under the terms of the GNU General Public               #
# License as published by the Free Software Foundation; either      #
# version 2 of the License, or (at your option) any later version.  #
#                                                                   #
# This program is distributed in the hope that it will be useful,   #
# but WITHOUT ANY WARRANTY; without even the implied warranty of    #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU #
# General Public License for more details.                          #
#                                                                   #
# You should have received a copy of the GNU General Public         #
# License along with this program; if not, write to the             #
# Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor,  #
# Boston, MA 02110-1301 USA                                         #
#                                                                   #
# Authored by: Raí B. Toffoletto <rai@toffoletto.me>                #
#                                                                   #
#####################################################################

import os, sys
import shutil
import subprocess

first_alert = input (' This script will install a new minecraft server\n' \
                    + ' in your ~/.minecraft-server folder.\n' \
                    + ' ** ANY DATA IN THIS DIRECTORY WILL BE DESTROYED **\n\n' \
                    + ' -- Would you like to proceed? [y/n]:')

if first_alert.lower ().strip () != 'y':
    print ('\n Exiting installer ...')
    sys.exit (0)

print ('\n Updating system and installing Java : \n ')
subprocess.check_call (['sudo', 'apt-get', 'update'])
subprocess.check_call (['sudo', 'apt-get', 'dist-upgrade', '-y'])
subprocess.check_call (['sudo', 'apt-get', 'install', '-y', 'openjdk-8-jdk', 'wget'])

print ('\n \n Preparations done. \n')
server_version = input (' Please, select the minecraft version to install (i.e. 1.15.2): ')

# Main list mantained by https://mcversions.net/

server_url = {
    '1.15.2' : 'https://launcher.mojang.com/v1/objects/bb2b6b1aefcd70dfd1892149ac3a215f6c636b07/server.jar',
    '1.15.1' : 'https://launcher.mojang.com/v1/objects/4d1826eebac84847c71a77f9349cc22afd0cf0a1/server.jar',
    '1.15' : 'https://launcher.mojang.com/v1/objects/e9f105b3c5c7e85c7b445249a93362a22f62442d/server.jar',
    '1.14.4' : 'https://launcher.mojang.com/v1/objects/3dc3d84a581f14691199cf6831b71ed1296a9fdf/server.jar',
    '1.14.3' : 'https://launcher.mojang.com/v1/objects/d0d0fe2b1dc6ab4c65554cb734270872b72dadd6/server.jar',
    '1.14.2' : 'https://launcher.mojang.com/v1/objects/808be3869e2ca6b62378f9f4b33c946621620019/server.jar',
    '1.14.1' : 'https://launcher.mojang.com/v1/objects/ed76d597a44c5266be2a7fcd77a8270f1f0bc118/server.jar',
    '1.14' : 'https://launcher.mojang.com/v1/objects/f1a0073671057f01aa843443fef34330281333ce/server.jar',
    '1.13.2' : 'https://launcher.mojang.com/v1/objects/3737db93722a9e39eeada7c27e7aca28b144ffa7/server.jar',
    '1.13.1' : 'https://launcher.mojang.com/v1/objects/fe123682e9cb30031eae351764f653500b7396c9/server.jar',
    '1.13' : 'https://launcher.mojang.com/v1/objects/d0caafb8438ebd206f99930cfaecfa6c9a13dca0/server.jar',
    '1.12.2' : 'https://launcher.mojang.com/v1/objects/886945bfb2b978778c3a0288fd7fab09d315b25f/server.jar',
    '1.12.1' : 'https://launcher.mojang.com/v1/objects/561c7b2d54bae80cc06b05d950633a9ac95da816/server.jar',
    '1.12' : 'https://launcher.mojang.com/v1/objects/8494e844e911ea0d63878f64da9dcc21f53a3463/server.jar',
    '1.11.2' : 'https://launcher.mojang.com/v1/objects/f00c294a1576e03fddcac777c3cf4c7d404c4ba4/server.jar',
    '1.11.1' : 'https://launcher.mojang.com/v1/objects/1f97bd101e508d7b52b3d6a7879223b000b5eba0/server.jar',
    '1.11' : 'https://launcher.mojang.com/v1/objects/48820c84cb1ed502cb5b2fe23b8153d5e4fa61c0/server.jar',
    '1.10.2' : 'https://launcher.mojang.com/v1/objects/3d501b23df53c548254f5e3f66492d178a48db63/server.jar',
    '1.10.1' : 'https://launcher.mojang.com/v1/objects/cb4c6f9f51a845b09a8861cdbe0eea3ff6996dee/server.jar',
    '1.10' : 'https://launcher.mojang.com/v1/objects/a96617ffdf5dabbb718ab11a9a68e50545fc5bee/server.jar'
}

wget_url = server_url.get (server_version, 'invalid')

if wget_url == 'invalid':
    print ('\n Invalid server version... aborting')
    sys.exit (0)

subprocess.check_call (['wget', wget_url])

print ('\n \n Creating server folder and installing files. \n')
current_folder = os.getcwd ()
server_folder = os.path.join (os.getenv ("HOME"), '.minecraft-server')

if not os.path.exists (server_folder):
    os.makedirs (server_folder)
    print (' Folder', server_folder, 'created.')
else:
    print (' Folder', server_folder, 'alread exists... cleaning-up!\n')
    for file in os.listdir (server_folder):
        file_path = os.path.join (server_folder, file)
        try:
            if os.path.isfile (file_path):
                os.unlink (file_path)
            elif os.path.isdir (file_path):
                shutil.rmtree (file_path)
        except Exception as e:
            print ('Error during clean-up :', e)
            sys.exit (0)

print (' .. copying server.jar')
shutil.copy2 (os.path.join (current_folder, 'server.jar'), server_folder)

print (' .. creating eula.txt')
eula_file = open (os.path.join (server_folder, 'eula.txt'), 'w')
eula_file.write ('eula=true')
eula_file.close ()

print (' .. creating startup.sh')
startup_file = open (os.path.join (server_folder, 'startup.sh'), 'w')
startup_file.write ('#!/bin/bash\n')
startup_file.write ('java -Xmx3072M -Xms1024M -jar ')
startup_file.write (os.path.join (server_folder, 'server.jar'))
startup_file.write (' nogui\n')
startup_file.close ()
os.chmod (os.path.join (server_folder, 'startup.sh'), 0o755)

print (' .. creating ops.json\n')
ops_uuid = input ('   Please insert your minecraft UUID: ').lower ().strip ()
ops_username = input ('   Please insert your minecraft username: ').lower ().strip ()
ops_file = open (os.path.join (server_folder, 'ops.json'), 'w')
ops_file.write ('[\n  {\n    "uuid": "')
ops_file.write (ops_uuid)
ops_file.write ('",\n    "name": "')
ops_file.write (ops_username)
ops_file.write ('",\n    "level": 4,\n    "bypassesPlayerLimit": true\n  }\n]\n')
ops_file.close ()

print ('\n\n Configuring minecraft world:\n ** Please type all options correctly! **')
motd = input (' + Server SHORT description: [A Minecraft Server] ').lower().strip()
server_port = input (' + Server Port: [25565] ').lower ().strip ()
max_players = input (' + Max number of players alowed: [20] ').lower ().strip ()
white_list = input (' + Allow only whited listed? [true/false] ').lower ().strip ()
gamemode = input (' + Gamemode: [survival/creative/adventure/spectator] ').lower ().strip ()
hardcore = input (' + Hardcore mode? [true/false] ').lower ().strip ()
difficulty = input (' + Difficulty level: [peaceful/easy/normal/hard] ').lower ().strip ()
level_seed = input (' + World Seed: [empty for random] ').lower ().strip ()
level_type = input (' + World Type: [default/flat/largebiomes/amplified/buffet] ').lower().strip ()
spawn_monsters = input (' + Spawn Monsters? [true/false] ').lower ().strip ()
spawn_animals = input (' + Spawn Animals? [true/false] ').lower ().strip ()
spawn_npcs = input (' + Spawn Villagers? [true/false] ').lower ().strip ()
generate_structures = input (' + Generate Structures? [true/false] ').lower ().strip ()
allow_nether = input (' + Allow Nether? [true/false] ').lower ().strip ()
spawn_protection = input (' + Spawn protection area: [16]').lower ().strip ()
max_build_height = input (' + Max build height: [256] ').lower ().strip ()
view_distance = input (' + View Distance: [10] ').lower().strip()
allow_flight = input (' + Allow in-game flight? [true/false] ').lower ().strip ()
#Set file:
properties = open (os.path.join (server_folder, 'server.properties'), 'w')
properties.write ('allow-flight='+allow_flight+'\n')
properties.write ('allow-nether='+allow_nether+'\n')
properties.write ('difficulty='+difficulty+'\n')
properties.write ('gamemode='+gamemode+'\n')
properties.write ('generate-structures='+generate_structures+'\n')
properties.write ('hardcore='+hardcore+'\n')
properties.write ('level-seed='+level_seed+'\n')
properties.write ('level-type='+level_type+'\n')
properties.write ('max-build-height='+max_build_height+'\n')
properties.write ('max-players='+max_players+'\n')
properties.write ('motd='+motd+'\n')
properties.write ('server-port='+server_port+'\n')
properties.write ('spawn-monsters='+spawn_monsters+'\n')
properties.write ('spawn-animals='+spawn_animals+'\n')
properties.write ('spawn-npcs='+spawn_npcs+'\n')
properties.write ('spawn-protection='+spawn_protection+'\n')
properties.write ('view-distance='+view_distance+'\n')
properties.write ('white-list='+white_list+'\n')
properties.write ('broadcast-console-to-ops=true\n')
properties.write ('broadcast-rcon-to-ops=true\n')
properties.write ('function-permission-level=2\n')
properties.write ('enforce-whitelist=false\n')
properties.write ('use-native-transport=true\n')
properties.write ('snooper-enabled=false\n')
properties.write ('query.port=25565\n')
properties.write ('server-ip=\n')
properties.write ('resource-pack-sha1=\n')
properties.write ('resource-pack=\n')
properties.write ('rcon.password=\n')
properties.write ('rcon.port=25575\n')
properties.write ('pvp=true\n')
properties.write ('prevent-proxy-connections=false\n')
properties.write ('player-idle-timeout=0\n')
properties.write ('op-permission-level=4\n')
properties.write ('online-mode=true\n')
properties.write ('network-compression-threshold=256\n')
properties.write ('max-world-size=29999984\n')
properties.write ('max-tick-time=60000\n')
properties.write ('level-name=world\n')
properties.write ('generator-settings=\n')
properties.write ('force-gamemode=true\n')
properties.write ('enable-rcon=false\n')
properties.write ('enable-query=false\n')
properties.write ('enable-command-block=false\n')
properties.close ()

print ('\n\n Creating system services ...\n')
systemd_service = open (os.path.join (server_folder, 'mc_server.service'), 'w')
systemd_service.write ('[Unit]\nDescription=Minecraft Vanilla Server\n\n[Service]\nType=simple\n')
systemd_service.write ('ExecStart=/bin/bash ')
systemd_service.write (os.path.join (server_folder, 'startup.sh'))
systemd_service.write ('\n\n[Install]\nWantedBy=multi-user.target\n')
systemd_service.close ()

subprocess.check_call (['sudo', 'cp', \
                        os.path.join (server_folder, 'mc_server.service'), \
                        '/etc/systemd/system/mc_server.service'])
subprocess.check_call (['sudo', 'chmod', '644', '/etc/systemd/system/mc_server.service'])
subprocess.check_call (['sudo', 'systemctl', 'enable', 'mc_server.service'])

print ('\n\n Installation done!!\n\n   To start your server just run:\n   sudo systemctl enable mc_server')
