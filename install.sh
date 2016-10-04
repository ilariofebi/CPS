#!/usr/bin/env bash

cp -a pull.py /usr/local/bin/pull
if [[ $(uname) == 'Darwin' ]]; then
    cp -a shot3.py /usr/local/bin/shot
else
    cp -a shot.py /usr/local/bin/shot
fi

chmod 755 /usr/local/bin/pull
chmod 755 /usr/local/bin/shot