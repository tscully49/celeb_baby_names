import pandas as pd
import us

names1 = pd.read_csv('data/stateNames1.csv')
names2 = pd.read_csv('data/stateNames2.csv')
df = pd.concat([names1, names2])

for year in range(1910,1954):
    for state in us.states.STATES:
        print("Status: " + str(year) + " " + state.abbr)
        rel_freq = 0
        names = df[(df.Year == year) & (df.State == state.abbr)]
        for i, name in names.iterrows():
            rel_freq += int(name['Count'])
        for i, name in names.iterrows():
            name['rel_freq'] = int(name['Count']) / rel_freq

df.to_csv('output/relFreqNames.csv')
