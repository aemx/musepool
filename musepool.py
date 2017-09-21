from random import shuffle

def parse(song):
    return (song.strip('\n')).split(' --- ')

listParsed = []

with open('data.mspl') as f:
    listSongs = f.readlines()
    for line in listSongs:
        listParsed.append(parse(line))

shuffle(listParsed)

for song in listParsed:
    print('[' + song[0] + '] ' + song[1] + ' - ' + \
    song[2] + ' [' + song[3] + ']')