import pandas as pd
import numpy as np
from tabulate import tabulate
import json
df = pd.read_excel("Financial_Report Apple.xlsx",sheet_name="CONDENSED CONSOLIDATED STATEMEN",engine="openpyxl")
df1 = pd.read_excel("Financial_Report (17).xlsx",sheet_name="CONDENSED CONSOLIDATED STATEMEN",engine='openpyxl')

# Q2
print(tabulate(df,headers='keys',tablefmt='grid'))

new_row = pd.DataFrame([["summary"] + [np.nan] * (df.shape[1] - 1)], columns=df.columns)

df = pd.concat([ new_row, df.iloc[1:]]).reset_index(drop=True)


df.replace({'': np.nan, '\xa0': np.nan}, inplace=True)

is_headings=df.iloc[:,1:].isna().all(axis=1) & df.iloc[:, 0].notna()

grouped_ids=is_headings.cumsum()

heading_names=df.loc[is_headings,df.columns[0]].reset_index(drop=True)

sub_keys=df.loc[~is_headings].reset_index(drop=True)

grouped_ids=grouped_ids[~is_headings].reset_index(drop=True)

sub_keys['section'] = grouped_ids.map(lambda x: heading_names[x-1] if x <= len(heading_names) else np.nan)
print(sub_keys)
sub_keys['combined_key'] =  sub_keys.iloc[:, 0] + "_" + sub_keys['section'] 

result = dict(zip(sub_keys['combined_key'], sub_keys.iloc[:, 1]))

print(tabulate(df1,headers='keys',tablefmt='grid'))
new_row=pd.DataFrame([['summary'] + [np.nan]*(df1.shape[1]-1)] , columns=df1.columns)
df1 = pd.concat([new_row,df1.iloc[1:]]).reset_index(drop=True)
df1.replace({'':np.nan,'\xa0':np.nan},inplace=True)
is_heading1=df1.iloc[:,1:].isna().all(axis=1) & df1.iloc[: , 0].notna()
grouped_ids1=is_heading1.cumsum()

heading_names1=df1.loc[is_heading1,df1.columns[0]].reset_index(drop=True)
sub_keys1=df1.loc[~is_heading1].reset_index(drop=True)

grouped_ids1=grouped_ids1[~is_heading1].reset_index(drop=True)

sub_keys1['section1']=grouped_ids1.map(lambda x:heading_names1[x-1] if x <= len(heading_names1) else np.nan)
sub_keys1['combined-keys1'] = sub_keys1.iloc[:,0] + '_' + sub_keys1['section1']


result1=dict(zip(sub_keys1['combined-keys1'] , sub_keys1.iloc[: , 1]))
print(json.dumps(result, indent=4))
print(json.dumps(result1 , indent=4))


search_item=90753

# for key , value in result1.items():
#     if value == search_item:
#         print(f"{key}")
#         if key in result:
#             print(result.get(key))

d1={v:k for k , v in result1.items()}
print(d1.get(90753))
res=d1.get(search_item)
print(result.get(res))
