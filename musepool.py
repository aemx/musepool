from os import execl
from random import shuffle

def parse(song):
    return (song.strip('\n')).split(' --- ')

def getSec(time):
    mm, ss = time.split(':')
    return (int(mm) * 60) + int(ss)

def INVgetSec(time):
    mm = str(int(time / 60))
    ss = str("%02d" % (time % 60))
    return (mm + ':' + ss)

listParsed = []

with open('data.mspl') as f:
    listSongs = f.readlines()
    for line in listSongs:
        listParsed.append(parse(line))

shuffle(listParsed)
runtime = 0

for song in listParsed:
    print('[' + song[0] + '] ' + song[1] + ' - ' + \
    song[2] + ' [' + str(getSec(song[3])) + ']')
    runtime += getSec(song[3])
    if runtime >= 3180:
        print('\x1b[1A' + '\x1b[2K' + '\x1b[1A')
        runtime -= getSec(song[3])
        continue
    elif runtime >= 3060:
        print('Total runtime: ' + INVgetSec(runtime))
        break
    elif song == listParsed[-1]:
        # print('Trying again...')
        # execl('python musepool.py')
    else:
        continue