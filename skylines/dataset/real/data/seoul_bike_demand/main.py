import pandas as pd

df = pd.read_csv('seoul_bike_demand.csv')
df.dropna(inplace=True)

df['Holiday'] = df['Holiday'].replace({"No Holiday": 0, "Holiday": 1})
df['Functioning Day'] = df['Functioning Day'].replace({"Yes": 0, "No": 1})

df.drop(columns=['Seasons'], inplace=True)
df.to_csv('seoul_bike_demand.csv', index=False)