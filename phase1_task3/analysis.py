f = open('bm25_stemming.txt', 'r')

fs = open('../phase1_task1/bm25.txt', 'r')
stemdict = {}
dict = {}
for line in f.readlines():
    line = line.split()
    if len(line) == 0:
        continue
    if line[0] in stemdict:
        stemdict[line[0]].append(line[2])
    else:
        stemdict[line[0]] = []
        stemdict[line[0]].append(line[2])

for line in fs.readlines():
    line = line.split()
    if len(line) == 0:
        continue
    if line[0] in dict:
        dict[line[0]].append(line[2])
    else:
        dict[line[0]] = []
        dict[line[0]].append(line[2])
count = 0
sl = 0
for file in stemdict['24']:
    sl += 1
    if sl > 15:
        break
    if file in dict['24']:
        count += 1
print(count)