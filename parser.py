def parse(song):
    return song.split('~')

prompt = input('Parse a song: ')

print('Genre: ' + parse(prompt)[0])
print('Artist: ' + parse(prompt)[1])
print('Song: ' + parse(prompt)[2])
print('Length: ' + parse(prompt)[3])
print('Key: ' + parse(prompt)[4])