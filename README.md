# CPS
Clay Pigeon Shooting is the **simplest way to transfering file or directory between hosts on a lan**.

CPS has been designed to operate in virtual networks as **lxcbr** (Linux containers) or in **Docker containers networking**, but it can work on any LAN.

CPS uses only **Python standard libraries** and does not use any transport protocol (http or ftp). 
CPS operates by using only raw sockets to **maximize the performance of transfert**.

In addition CPS does **not require host infomration** (it destination, source it) using a broadcast packets and ensures security 
(on small networks) **without using passwords** (raw socket keep opened for few seconds)

##Install:
```
sh install.sh
```

##Usage:
On the host where the file or directory resides (puller):
```bash
pull -p <filename|directory>
```

On destination host simply (shooter):
```bash
shot
```

## Puller help
```
usage: pull.py [-h] --pigeon PIGEON [--talkative]
               [--gravity {zero,moon,earth,sun}]
Puller options:

optional arguments:
  -h, --help show this help message and exit
  --pigeon PIGEON, -p PIGEON
                        What would you like to pull
                        If the pigeon is a directory, pull.py will create a tarball.

  --talkative, -t Commentator comments
                        More "t" will insert more babbler be the commentator

  --gravity {zero,moon,earth,sun}, -g {zero,moon,earth,sun}
                        More gravity means shorter firing times
                        In case of zero gravity, pigeon will keep flying, in case of sun gravity you will have only a second to shoot
```

##Unstall:
```
sh uninstall.sh
```

##Video Example:
[![CPS](http://img.youtube.com/vi/EQBo8qqyDhc/0.jpg)](http://www.youtube.com/watch?v=EQBo8qqyDhc)
