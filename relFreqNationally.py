import pandas as pd

df = pd.read_csv('data/NationalNames.csv')

for year in range(1880, 1989):
    print("Status: " + str(year))
    rel_freq = 0
    names = df[(df.Year == year)]
    for i, name in names.iterrows():
        rel_freq += int(name['Count'])
    for i, name in names.iterrows():
        name['rel_freq'] = int(name['Count']) / rel_freq

df.to_csv('output/relFreqNationalNames.csv')
