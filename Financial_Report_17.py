import pandas as pd
import numpy as np
import json
from tabulate import tabulate
df1 = pd.read_excel("Financial_Report (17).xlsx",sheet_name="CONDENSED CONSOLIDATED STATEMEN",engine='openpyxl')
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


result1=dict(zip(sub_keys1['combined-keys1'] , sub_keys1.iloc[: , 2]))
print(json.dumps(result1 , indent=4))
