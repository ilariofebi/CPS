#!/usr/bin/env python

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
## Shot ##
##########

import sys
import random
import socket
import json
import os

shot_port = random.randrange(19000, 19999)
bc_port = 50000

print "Shot!"
try:
    ## Phase 1
    ## Send shot_port by broadcast
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(('', 0))
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    s.sendto(str(shot_port), ('<broadcast>', bc_port))
    s.close()

    ## Phase 2
    ## Open socket on shot_port
    sh = socket.socket()
    sh.settimeout(5)
    sh.bind(('', shot_port))
    sh.listen(1)  # Acept 1 connection
    sc, address = sh.accept()

    ## Receive file metainfo (json format)
    json_info = sc.recv(1024)
    info = json.loads(json_info)
    filename = info['filename'] + '.shot'

    ## Phase 3
    ## Receive file
    i = 1
    f = open(filename, 'wb')  # open in binary
    l = sc.recv(1024)

    while (l):
        i = i + 1
        f.write(l)
        l = sc.recv(1024)
        if(i % 100 == 0):
            sys.stdout.write('.')
    f.close()
    sc.close()
except socket.timeout:
    print("I do not see pigeon in the neighborhood")

###
## Post operations
try:
    ## Check if file exist
    if (os.path.isfile(info['filename'])):
        #this file already exist
        for i in range(1, 1000):
            newname = info['filename'] + '.' + str(i)
            if os.path.isfile(newname):
                continue
            else:
                os.rename(filename, newname)
                break
    else:
        #this file do not exist
        os.rename(filename, info['filename'])

    print "\nHit!!"
except:
    print ("We made some mistakes by cooking the pigeon :( ")