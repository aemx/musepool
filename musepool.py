def parse(song):
    return (song.strip('\n')).split(' ~ ')

listParsed = []

with open('mspl/main.mspl') as f:
    listSongs = f.readlines()
    for line in listSongs:
        listParsed.append(parse(line))

print(listParsed)