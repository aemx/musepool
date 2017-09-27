import os
import re
from random import shuffle
import sys

def getSec(time):
    mm, ss = time.split(':')
    return (int(mm) * 60) + int(ss)

def INVgetSec(time):
    mm = str(int(time / 60))
    ss = str("%02d" % (time % 60))
    return (mm + ':' + ss)

def traverse(key):
    num, key = re.findall('\d+|\D+', key)
    num = int(num)

    if num == 12:
        fNum, bNum = '1', '11'

    elif num == 1:
        fNum, bNum = '2', '12'

    else:
        fNum, bNum = str(num + 1), str(num - 1)

    if key == 'A':
        nKey = 'B'

    else:
        nKey = 'A'

    return [bNum + key, str(num) + key, fNum + key, str(num) + nKey]

def getPlaylist(lis, runtimeMax, runtimeMin):
    e = 0

    while e == 0:
        shuffle(lis)
        genres, lastTraverse, playlist, returnstr = [], [], [], []
        runtime = 0

        for idx, song in enumerate(lis):
            returnstr.append('[' + song[4] + '] [' + \
            song[0] + '] ' + song[1] + ' - ' + song[2] + ' [' + \
            str(getSec(song[3])) + ']\n')
            lis.remove(song)
            runtime += getSec(song[3])
            genres.append(song[0])

            if idx == 0:
                pass

            else:
                if song[4] in lastTraverse:
                    pass

                else:
                    returnstr.remove('[' + song[4] + '] [' + \
                    song[0] + '] ' + song[1] + ' - ' + song[2] + ' [' + \
                    str(getSec(song[3])) + ']\n')
                    lis.append(song)
                    runtime -= getSec(song[3])
                    genres.remove(song[0])

                    if idx == len(lis) - 1:
                        break

                    else:
                        continue

            if runtime >= runtimeMax:
                returnstr.remove('[' + song[4] + '] [' + \
                song[0] + '] ' + song[1] + ' - ' + song[2] + ' [' + \
                str(getSec(song[3])) + ']\n')
                lis.append(song)
                runtime -= getSec(song[3])
                genres.remove(song[0])

                if idx == len(lis) - 1:
                    break

                else:
                    continue

            elif runtime >= runtimeMin:
                returnstr.append('\n[Total runtime: ' + \
                INVgetSec(runtime) + ']\n')

                if len(genres) > 4:
                    e = 1
                    return ''.join(returnstr)
                    break
                
                else:
                    break

            elif idx == len(lis) - 1:
                break

            else:
                lastTraverse = traverse(song[4])

os.system('clear')

print('Please select an option:')
print('  o - output')
print('  i - input')
print('  x - exit\n')

while True:
    try:
        selectIO = input('>>> ')

    except ValueError:
        print('\nIncorrect operation specified. Please retry.\n')
        continue

    if selectIO == 'o':
        os.system('clear')
        listParsed = []

        with open('data.mspl') as f:
            listSongs = f.readlines()

            for line in listSongs:
                listParsed.append(line.strip('\n').split('; '))

        print('Playlist 1:')
        print('=' * 80)
        print(getPlaylist(listParsed, 1560, 1500))

        print('Playlist 2:')
        print('=' * 80)
        print(getPlaylist(listParsed, 1740, 1680))
        break

    elif selectIO is 'i':
        os.system('clear')

        inputGenre = input('Enter the genre of this song: ')
        inputArtist = input('Enter a list of artists featured in this ' + \
        'song, separated by a comma: ')
        inputTitle = input('Enter the title of this song: ')
        inputLen = input('Enter the length of this song in [MM:SS] format: ')
        inputKey = input('Enter the key of the song in Camelot format: ')

        print('\n[' + inputKey + '] [' + inputGenre + '] ' + inputArtist + \
        ' - ' + inputTitle + ' [' + inputLen + ']\n')

        while True:
            selectInput = input('Is this okay? [Y/n] ')

            if selectInput.lower() in ('yes', 'ye', 'y', ''):
                with open('data.mspl', 'a') as f:
                    f.write('\n' + inputGenre + '; ' + inputArtist + '; ' +
                    inputTitle + '; ' + inputLen + '; ' + inputKey)
                print()
                break

            elif selectInput.lower() in ('no', 'n'):
                print('\nExiting...\n')
                sys.exit()

            else:
                print('\nPlease respond with "yes/y" or "no/n".\n')
                continue
        break

    elif selectIO is 'x':
        print('\nExiting...\n')
        sys.exit()
    
    else:
        print('\nIncorrect operation specified. Please retry.\n')
        continue