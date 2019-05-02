import csv
nba_data = []
mod_data = []
with open('SalariesData.txt','r') as file:
    data = csv.DictReader(file)
    [nba_data.append(x) for x in data]

for player in nba_data:
    if player['Player'] in [x['Player'] for x in mod_data]:
        pass
    else:
        mod_data.append(player)

#[print(x['Player'],',', x['Tm']) for x in mod_data]
num_stats = 4
stats = mod_data[0].keys()

for stat in stats:
    if stat == next(reversed(stats)):
        print(stat)
    else:
        print(stat+',', end = '')
        
for player in mod_data:
    for stat in stats:
        if stat == next(reversed(stats)):
            print(player[stat])
        else:
            print(player[stat]+',', end = '')



