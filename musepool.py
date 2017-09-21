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

def getPlaylist(lis, runtimeMax, runtimeMin):
    playlist = []
    runtime = 0

    for idx, song in enumerate(lis):
        print('[' + song[0] + '] ' + song[1] + ' - ' + \
        song[2] + ' [' + str(getSec(song[3])) + ']')
        lis.remove(song)
        runtime += getSec(song[3])

        if runtime >= runtimeMax:
            print('\x1b[1A' + '\x1b[2K' + '\x1b[1A')
            runtime -= getSec(song[3])
            lis.append(song)
            if idx == len(lis) - 1:
                print('FAILED')
                # restart
                break
            else:
                continue

        elif runtime >= runtimeMin:
            print('[Total runtime: ' + INVgetSec(runtime) + ']')
            break

        else:
            continue

listParsed = []

with open('data.mspl') as f:
    listSongs = f.readlines()

    for line in listSongs:
        listParsed.append(parse(line))

shuffle(listParsed)
print(len(listParsed))
getPlaylist(listParsed, 1500, 1440)
print(len(listParsed))
getPlaylist(listParsed, 1680, 1620)
print(len(listParsed))