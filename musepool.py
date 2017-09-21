import os
from random import shuffle
import sys

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
                os.system('clear')
                print('Failed to compile list. Try again.')
                sys.exit()

            else:
                continue

        elif runtime >= runtimeMin:
            print('=' * 80)
            print('[Total runtime: ' + INVgetSec(runtime) + ']\n')
            break

        else:
            continue

os.system('clear')
listParsed = []

with open('data.mspl') as f:
    listSongs = f.readlines()

    for line in listSongs:
        listParsed.append(parse(line))

shuffle(listParsed)

print('Playlist 1:')
print('=' * 80)
getPlaylist(listParsed, 1500, 1440)
print('Playlist 2:')
print('=' * 80)
getPlaylist(listParsed, 1680, 1620)