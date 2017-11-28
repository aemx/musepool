import os

os.system('clear')
listParsed = []

with open('data.mspl') as f:
    listRaw = f.readlines()

    for line in listRaw:
        listParsed.append(line.strip('\n').split('; '))

print(listParsed)