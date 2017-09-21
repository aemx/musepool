from random import shuffle

def parse(song):
    return (song.strip('\n')).split(' --- ')

def getSec(time):
    mm, ss = time.split(':')
    return str((int(mm) * 60) + int(ss))

listParsed = []

with open('data.mspl') as f:
    listSongs = f.readlines()
    for line in listSongs:
        listParsed.append(parse(line))

shuffle(listParsed)

for song in listParsed:
    print('[' + song[0] + '] ' + song[1] + ' - ' + \
    song[2] + ' [' + getSec(song[3]) + ']')