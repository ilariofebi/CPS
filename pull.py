#!/usr/bin/env python3

'''
  This file is part of Clay Pigeon Shooting

  Clay Pigeon Shooting is free software: you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation, either version 3 of the License, or
  (at your option) any later version.

  Clay Pigeon Shooting is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.

  You should have received a copy of the GNU General Public License
  along with Clay Pigeon Shooting.  If not, see <http://www.gnu.org/licenses/>.
'''

##########
## Pull ##
##########

import sys
import socket
import json
import os
import time
import tarfile
import tempfile

info = {}
temp_files = []
bc_port = 50000  # broadcast port


def comment(comment, talk):
    global talkative
    if (talkative >= talk):
        print(comment)


def make_tarfile(source_dir):
    f = tempfile.mkstemp()
    comment('I recommended using a machine gun', 2)
    comment('creating temporary file: ' + str(f), 3)
    output_filename = f[1]
    with tarfile.open(output_filename, "w:gz") as tar:
        tar.add(source_dir, arcname=os.path.basename(source_dir))
    return output_filename


########################
## Arguments handling ##
########################

###
# in the absence of argparse or ultrafast method as you can use the
# use ./pull.py filename
if (len(sys.argv) == 2 and os.path.isfile(sys.argv[1])):
    talkative = 0
    pigeon = sys.argv[1]
    gravity = 'earth'
else:
    # Parse degli argomenti
    try:
        import argparse
    except ImportError:
        print("Module argparse missed")
        print("sudo pip install argparse")
        print(("or use %s fileanme" % sys.argv[0]))

        sys.exit(1)

    parser = argparse.ArgumentParser(description='Puller')
    parser.add_argument('--pigeon', '-p', required=True,
                        help='What would you like to pull')
    parser.add_argument('--talkative', '-t', action='count', default=0,
                        help='Commentator comments')
    parser.add_argument('--gravity', '-g',
                        choices=['zero', 'moon', 'earth', 'sun'],
                        default='earth',
                        help='In case of zero gravity, will keep flying')

    args = parser.parse_args()
    talkative = args.talkative
    pigeon = args.pigeon
    gravity = args.gravity

comment('talkative value is: ' + str(talkative), 1)

# Gravity handling
if(gravity == 'zero'):
    tout = 100000
    comment('We are in the absence of gravity', 1)
elif(gravity == 'moon'):
    comment('We are on the moon', 1)
    tout = 60
elif(gravity == 'sun'):
    comment('We are on the sun', 1)
    tout = 1
else:
    comment('We are on earth', 1)
    tout = 10


# The pigeon is a file or directory?
if (os.path.isfile(pigeon)):
    comment('The pigeon is alone', 2)
    info['filename'] = pigeon
    sendfile = info['filename']
elif (os.path.isdir(pigeon)):
    comment('is a storm of pigeons!', 2)
    info['filename'] = pigeon + '.tgz'
    sendfile = make_tarfile(pigeon)
    temp_files.append(sendfile)


try:
    ## Phase 1
    ## Open broadcast socket
    comment('Puuuull', 0)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ## Waiting first shot
    s.settimeout(int(tout))
    s.bind(('', bc_port))

    shot_port, wherefrom = s.recvfrom(1500, 0)
    comment('IP: ' + str(repr(wherefrom)), 2)
    comment('shot port: ' + str(shot_port), 2)
    s.close()

    pull_info = (shot_port, wherefrom[0])
    comment('pull_info: ' + str(pull_info), 3)

    shot_port = int(pull_info[0])
    ip_server = pull_info[1]

    c = socket.socket()

    ## Phase 2
    ## Sending file metainfo (json metainfo)
    time.sleep(1)
    c.connect((ip_server, shot_port))
    c.sendall(json.dumps(info).ljust(1024).encode('ascii'))

    ## Phase 3
    # Sending file
    f = open(sendfile, "rb")
    c.sendall(f.read())
    c.close()

    # Clean Temp file
    for i in temp_files:
        comment('deleting temporary file: ' + str(i), 3)
        os.unlink(i)

    comment("GREAT!! The pigeon was shot!", 0)
except socket.timeout:
    comment("Missed :(", 0)
except socket.error:
    comment("Dud!!", 0)
