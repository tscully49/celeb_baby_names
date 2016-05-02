import pandas as pd
import us

# load the two two name data sets and then combine them into one
names1 = pd.read_csv('data/stateNames1.csv')
names2 = pd.read_csv('data/stateNames2.csv')

df = pd.concat([names1, names2])

# we want to look at the rate of change of a name by year, so we need to look at a name in a particular year and see
# what the change is from the previous year

rate_changes = []

# start the year +1 from the dataset because we want to look at the change but can't for the first year
for year in list(range(1911, 1953)):
    for state in us.states.STATES:
        names = df[(df.Year == year) & (df.State == state.abbr)]
        for i, row in names.iterrows():
            name = row['Name']
            count = row['Count']
            gender = row['Gender']
            prev = df[(df.Year == (year - 1)) & (df.Name == name) & (df.State == state.abbr) & (df.Gender == gender)]
            change = 'NA'
            if len(prev) > 0:
                prev_count = prev['Count']
                change = count - prev_count
            rate_changes.append(change)

df['change'] = rate_changes

df.to_csv('output/StateNameChange.csv')
