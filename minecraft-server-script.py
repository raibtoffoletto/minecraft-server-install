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

import os, sys, time
import shutil
import subprocess
import json

servers = {}
# Main list mantained by https://mcversions.net/
with open('servers.json') as json_file:
    servers: dict = json.load(json_file)

def loading_cmd (message,waiting_cmd):
    while waiting_cmd.poll () is None:
        chars = "|/—\\"
        for char in chars:
            time.sleep (0.3)
            sys.stdout.write ('\r ' + message + ' ' + char)
            sys.stdout.flush ()
    if waiting_cmd.returncode > 0:
        print ('\n Error while running command:')
        print (waiting_cmd.stderr.read ().decode ())
        sys.exit (1)
    sys.stdout.write ('\r ' + message + ', done!\n')

def ask_question (message, answers = [], strict = False):
    user_input = (input (message)).lower ().strip ()
    if len(answers) != 0:
        if strict:
            while not user_input in answers:
                user_input = (input (message)).lower ().strip ()
            return user_input

        return (user_input if user_input != "" else answers[0])
    else:
        while user_input == "":
            user_input = (input (message)).lower ().strip ()
        return user_input

first_alert = ask_question (" This script will install a new minecraft server\n" \
                    + " in your ~/.minecraft-server folder.\n" \
                    + " ** ANY DATA IN THIS DIRECTORY WILL BE DESTROYED **\n\n" \
                    + " -- Would you like to proceed? [y/n]:", ['y','n'], True)

if first_alert.lower ().strip () != "y":
    print ("\n Exiting installer ...")
    sys.exit (0)

print ("\n Updating system and installing Java : \n ")
subprocess.check_call (['sudo', 'apt-get', 'update'])
subprocess.check_call (['sudo', 'apt-get', 'dist-upgrade', '-y'])
subprocess.check_call (['sudo', 'apt-get', 'install', '-y', 'openjdk-8-jdk', 'wget'])

print ("\n \n Preparations done. \n")
versions = list(servers.keys())
server_version = ask_question (" Please, select the minecraft version to install (%s ~ %s): "%(versions[0], versions[-1]),
                versions, True)

wget_server = subprocess.Popen (['wget','--no-check-certificate','-c', servers.get (server_version)], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
loading_cmd ('Getting minecraft-server.jar', wget_server)

print ("\n \n Creating server folder and installing files. \n")
current_folder = os.getcwd ()
server_folder = os.path.join (os.getenv ("HOME"), '.minecraft-server')

if not os.path.exists (server_folder):
    os.makedirs (server_folder)
    print (" Folder", server_folder, "created.")
else:
    print (" Folder", server_folder, "alread exists... cleaning-up!\n")
    for file in os.listdir (server_folder):
        file_path = os.path.join (server_folder, file)
        try:
            if os.path.isfile (file_path):
                os.unlink (file_path)
            elif os.path.isdir (file_path):
                shutil.rmtree (file_path)
        except Exception as e:
            print ("Error during clean-up : ", e)
            sys.exit (1)

print (" .. copying server.jar")
shutil.copy2 (os.path.join (current_folder, 'server.jar'), server_folder)

print (" .. copying coordinates.zip")
datapack_folder = os.path.join (server_folder, 'world/datapacks')
os.makedirs (datapack_folder)
shutil.copy2 (os.path.join (current_folder, 'coordinates.zip'), datapack_folder)

print (" .. creating eula.txt")
eula_file = open (os.path.join (server_folder, 'eula.txt'), 'w')
eula_file.write ('eula=true')
eula_file.close ()

print (" .. creating startup.sh")
startup_file = open (os.path.join (server_folder, 'startup.sh'), 'w')
startup_file.write ('#!/bin/bash\n')
startup_file.write ('java -Xmx3072M -Xms1024M -jar ')
startup_file.write (os.path.join (server_folder, 'server.jar'))
startup_file.write (' nogui\n')
startup_file.close ()
os.chmod (os.path.join (server_folder, 'startup.sh'), 0o755)

print (" .. creating ops.json \n")
ops_uuid = ask_question ('   Please insert your minecraft UUID: ')
ops_username = ask_question ('   Please insert your minecraft username: ')
ops_file = open (os.path.join (server_folder, 'ops.json'), 'w')
ops_file.write ('[\n  {\n    "uuid": "')
ops_file.write (ops_uuid)
ops_file.write ('",\n    "name": "')
ops_file.write (ops_username)
ops_file.write ('",\n    "level": 4,\n    "bypassesPlayerLimit": true\n  }\n]\n')
ops_file.close ()

print ("\n\n Configuring minecraft world: ")
motd = ask_question (' + Server SHORT description: [ex: A Minecraft Server] ')
server_port = ask_question (' + Server Port: [25565] ', ['25565'])
max_players = ask_question (' + Max number of players alowed: [20] ', ['20'])
white_list = ask_question (' + Allow only whited listed? [true/false] ', ['true','false'], True)
gamemode = ask_question (' + Gamemode: [survival/creative/adventure/spectator] ', ['survival', 'creative', 'adventure', 'spectator'], True)
hardcore = ask_question (' + Hardcore mode? [true/false] ', ['true','false'], True)
difficulty = ask_question (' + Difficulty level: [peaceful/easy/normal/hard] ', ['peaceful', 'easy', 'normal', 'hard'], True)
level_seed = input (' + World Seed: [empty for random] ').lower ().strip ()
level_type = ask_question (' + World Type: [default/flat/largebiomes/amplified/buffet] ', ['default', 'flat', 'largebiomes', 'amplified', 'buffet'], True)
spawn_monsters = ask_question (' + Spawn Monsters? [true/false] ', ['true','false'], True)
spawn_animals = ask_question (' + Spawn Animals? [true/false] ', ['true','false'], True)
spawn_npcs = ask_question (' + Spawn Villagers? [true/false] ', ['true','false'], True)
generate_structures = ask_question (' + Generate Structures? [true/false] ', ['true','false'], True)
allow_nether = ask_question (' + Allow Nether? [true/false] ', ['true','false'], True)
spawn_protection = ask_question (' + Spawn protection area: [16]', ['16'])
max_build_height = ask_question (' + Max build height: [256] ', ['256'])
view_distance = ask_question (' + View Distance: [10] ', ['10'])
allow_flight = ask_question (' + Allow in-game flight? [true/false] ', ['true','false'], True)

# Set file:
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

print ("\n\n Creating system services ...\n")
systemd_service = open (os.path.join (server_folder, 'mc_server.service'), 'w')
systemd_service.write ('[Unit]\nDescription=Minecraft Vanilla Server\n\n[Service]\nType=simple\n')
systemd_service.write ('WorkingDirectory=')
systemd_service.write (os.path.join (server_folder))
systemd_service.write ('\nExecStart=/bin/bash ')
systemd_service.write (os.path.join (server_folder, 'startup.sh'))
systemd_service.write ('\n\n[Install]\nWantedBy=multi-user.target\n')
systemd_service.close ()

subprocess.check_call (['sudo', 'cp', \
                        os.path.join (server_folder, 'mc_server.service'), \
                        '/etc/systemd/system/mc_server.service'])
subprocess.check_call (['sudo', 'chmod', '644', '/etc/systemd/system/mc_server.service'])
subprocess.check_call (['sudo', 'systemctl', 'enable', 'mc_server.service'])

print ("\n\n Installation done!!\n\n   To start your server just run:\n   sudo systemctl start mc_server")
