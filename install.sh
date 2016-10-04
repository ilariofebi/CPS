#!/usr/bin/env bash

HB=$(which python3 || which python2 || echo 'None')
if [[ $HB == 'None' ]]
 then
    echo 'python3 or python2 needed'
    exit 10
fi

echo "#!"$HB > /usr/local/bin/pull
grep -v '^#!' pull.py >> /usr/local/bin/pull
chmod 755 /usr/local/bin/pull

echo "#!"$HB > /usr/local/bin/shot
grep -v '^#!' shot.py >> /usr/local/bin/shot
chmod 755 /usr/local/bin/shot