import pandas as pd
from tabulate import tabulate
df = pd.read_excel("Financial_Report Apple.xlsx",sheet_name="CONDENSED CONSOLIDATED STATEMEN",engine="openpyxl")
print(tabulate(df,headers='keys',tablefmt='grid'))
col1=df.iloc[:,[0,1]]
col2=df.iloc[:,[0,2]]
col3=df.iloc[:,[0,3]]
col4=df.iloc[:,[0,4]]

print(df.columns.tolist(),"\n\n\n")
print("\n\nColumn 1 and 2\n\n")
print(col1.to_json())

print("\n\nColumn 1 and 3\n\n")
print(col2.to_json())

print("\n\nColumn 1 and 4\n\n")
print(col3.to_json())

print("\n\nColumn 1 and 5\n\n")
print(col4.to_json())

print("\n\n",col4.to_dict(orient='records'))

key_column=df.columns[0]
value_column=df.columns[1]
dict_values=dict(zip(df[key_column],df[value_column]))
print("\n\n Dict \n\n",dict_values)

result=df.groupby(df.columns[0])[df.columns[4]].apply(list).to_dict()
print("\n\nResult\n\n",result)

res=df.groupby(df.columns[1])[df.columns[0]].apply(list).to_json()
print("\n\nJson\n\n",res)
