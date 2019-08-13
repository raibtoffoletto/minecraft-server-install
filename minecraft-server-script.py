#!/usr/bin/env python3
# git clone script
# python3 script.py
import os, sys, shutil
import subprocess

# first_alert = input (' This script will install a new minecraft server\n in your ~/.minecraft-server folder.\n ** ANY DATA IN THIS DIRECTORY WILL BE DESTROYED **\n\n -- Would you like to proceed? [y/n]:')
# if first_alert.lower().strip() != 'y':
#     print ('\n Exiting installer ...')
#     sys.exit (0)

print ('\n Updating system and installing Java : \n ')
# subprocess.check_call (['sudo', 'apt-get', 'update'])
# subprocess.check_call (['sudo', 'apt-get', 'dist-upgrade', '-y'])
# subprocess.check_call (['sudo', 'apt-get', 'install', '-y', 'openjdk-8-jdk', 'wget'])

print ('\n \n Preparations done. \n')
server_version = input (' Please, select the minecraft version to install (i.e. 1.14.2): ')

server_url = {
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

# wget_url = server_url.get (server_version, 'invalid')

# if wget_url == 'invalid':
#     print ('\n Invalid server version... aborting')
#     sys.exit (0)

# subprocess.check_call (['wget', wget_url])

print ('\n \n Creating server folder and installing files. \n')
current_folder = os.getcwd ()
server_folder = os.path.join (os.getenv ("HOME"), '.minecraft-server')

if not os.path.exists(server_folder):
    os.makedirs(server_folder)
    print ('Folder', server_folder, 'created.')
else:
    print ('Folder', server_folder, 'alread exists... cleaning-up!')
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

print ('.. copying server.jar')
shutil.copy2 (os.path.join (current_folder, 'server.jar'), server_folder)

print ('.. creating eula.txt')
eula_file = open (os.path.join (server_folder, 'eula.txt'), 'w')
eula_file.write ('eula=true')
eula_file.close ()

print ('.. creating startup.sh')
startup_file = open (os.path.join (server_folder, 'startup.sh'), 'w')
startup_file.write ('#!/bin/bash\n')
startup_file.write ('java -Xmx3072M -Xms1024M -jar ')
startup_file.write (os.path.join (server_folder, 'server.jar'))
startup_file.write (' nogui\n')
startup_file.close ()
os.chmod (os.path.join (server_folder, 'startup.sh'), 755)








