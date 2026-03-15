import pandas as pd

df = pd.read_csv('_raw_covertype.csv', sep="\t")
print(df.head())
df.to_csv('covertype_10K_0.csv', index=False)