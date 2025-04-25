import pandas as pd
from tabulate import tabulate
df = pd.read_excel("Financial_Report Apple.xlsx",sheet_name="CONDENSED CONSOLIDATED STATEMEN",engine="openpyxl")
print(df.to_string)

print("Grid")
print(tabulate(df, headers='keys', tablefmt='grid'))


print("Simple")
print(tabulate(df.head(),headers='keys',tablefmt='simple'))

print("Plain")
print(tabulate(df.tail(),headers='keys',tablefmt='plain'))

print("Pipe")
print(tabulate(df, headers='keys', tablefmt='pipe'))

print("Pretty")
print(tabulate(df,headers='keys',tablefmt='pretty'))

print("Fancy Grid")
print(tabulate(df,headers='key',tablefmt='fancy_grid'))

print("Rst")
print(tabulate(df,headers='key',tablefmt='rst'))

print("github")
print(tabulate(df,headers='key',tablefmt='github'))

print("orgtbl")
print(tabulate(df,headers='key',tablefmt='orgtbl'))

print("jira")
print(tabulate(df,headers='key',tablefmt='jira'))

print("Presto")
print(tabulate(df,headers='key',tablefmt='presto'))

print("mediawiki")
print(tabulate(df,headers='key',tablefmt='mediawiki'))


print("mediawiki")
print(tabulate(df,headers='key',tablefmt='mediawiki'))

print("youtrack")
print(tabulate(df,headers='key',tablefmt='youtrack'))

print("Head")
print(df.head())

print("Tail")
print(df.tail())

print("Location iloc")
print(tabulate(df.iloc[0:2 , 0:2],headers='keys',tablefmt='grid'))

print("Location loc")
print(tabulate(df.loc[0:1, 'CONDENSED CONSOLIDATED STATEMENTS OF OPERATIONS (Unaudited) - USD ($) shares in Thousands, $ in Millions':'3 Months Ended'], headers='keys', tablefmt='grid'))

print("\n\n\n")
original_column=df.columns.tolist()
original_index=df.index.tolist()
print(original_column)
print(original_index)

df.columns=['A','B','C','D','E']
df=df.rename(index={0:'a',1:'b'})
print("\n\n\nRename columns",df.columns.tolist(),df.index.tolist())
print("iloc\n\n")
print(tabulate(df.iloc[0:2,0:2]))
print("loc\n\n")
print(tabulate(df.loc['a':'b','A':'B']))
df.columns=original_column
df.index=original_index
df=df.rename(index={0:'a',1:'b'},columns={'CONDENSED CONSOLIDATED STATEMENTS OF OPERATIONS (Unaudited) - USD ($) shares in Thousands, $ in Millions':'A'} )
print("Data after modifications")
print(df)

df.columns=original_column
df.index=original_index
print(df.to_string())


