import pandas as pd
import numpy as np
from tabulate import tabulate
import json
df = pd.read_excel("Financial_Report Apple.xlsx",sheet_name="CONDENSED CONSOLIDATED STATEMEN",engine="openpyxl")
print(tabulate(df,headers='keys',tablefmt='grid'))

new_row = pd.DataFrame([["Summary"] + [np.nan] * (df.shape[1] - 1)], columns=df.columns)

df = pd.concat([ new_row, df.iloc[1:]]).reset_index(drop=True)
print("NEw Column")
print(tabulate(df, headers='keys', tablefmt='grid'))

df.replace({'': np.nan, '\xa0': np.nan}, inplace=True)

is_headings=df.iloc[:,1:].isna().all(axis=1) & df.iloc[:, 0].notna()
print(is_headings)
grouped_ids=is_headings.cumsum()
print(grouped_ids)
heading_names=df.loc[is_headings,df.columns[0]].reset_index(drop=True)
print(heading_names)
sub_keys=df.loc[~is_headings].reset_index(drop=True)
print(sub_keys)
grouped_ids=grouped_ids[~is_headings].reset_index(drop=True)
print(grouped_ids)
sub_keys['section'] = grouped_ids.map(lambda x: heading_names[x-1] if x <= len(heading_names) else np.nan)
print(sub_keys)
sub_keys['combined_key'] = sub_keys['section'] + "_" + sub_keys.iloc[:, 0]


result = dict(zip(sub_keys['combined_key'], sub_keys.iloc[:, 1]))

print(json.dumps(result, indent=4))

search_item="Net sales"

for key , value in result.items():
    if key.find(search_item) != -1:
        print(f"{key}:{value}")
