import openpyxl
import json
import numpy as np
path='C:\PyTask\ExcelSheets\Apple-model-dummy.xlsx'
path1='C:\PyTask\ExcelSheets\Financial_Report (17).xlsx'
path2='C:\PyTask\ExcelSheets\Financial_Report Apple.xlsx'

wb=openpyxl.load_workbook(path , data_only=True)
wb1=openpyxl.load_workbook(path1)
wb2=openpyxl.load_workbook(path2)

name="CONDENSED CONSOLIDATED STATEMEN"

ws=wb.active
col=ws.max_column
rows=ws.max_row
print("\nColumns:",col ,"\nRow:",rows)
for i in range(6, rows+1):
    cell_obj=ws.cell(row=i,column=1).value
    cell_obj1=ws.cell(row=i,column=2).value
    print("\n",cell_obj,"\t\t\t\t\t\t\t",cell_obj1)
    

#Q2
ws2=wb1[name]
keys=[]
values=[]

print(ws2.title)
for i in ws2['A']:
    keys.append(i.value)

for row in ws2.iter_rows(min_row=3):
    other_cells = row[2]
    values.append(other_cells.value)

dict1=dict(zip(keys,values))
print(json.dumps(dict1,indent=4))

#Q3
print(wb2.sheetnames)
ws3=wb2[name]

keys1=[]
values1=[]
for i in ws3['A']:
    keys.append(i.value)
for i in ws3['B']:
    values.append(i.value)

dict2=dict(zip(keys1,values1))
print(json.dumps(dict2,indent=4))




headings = []  
sub_key=[]
keys=""
for row in ws2.iter_rows(min_row=3):  
    first_cell = row[0] 
    other_cells = row[1:]  
    
    if first_cell.value and all(
        (cell.value is None) or (str(cell.value).strip() == '') or (str(cell.value).strip() == '\u00a0')
        for cell in other_cells
    ):
        keys=first_cell.value
        headings.append(first_cell.value)
        
    else:
        sub_key.append(first_cell.value + "_" + keys)
print(sub_key)
print("Detected Headings:")
for heading in sub_key:
    print(heading)
dict3=dict(zip(sub_key,values))
print(json.dumps(dict3,indent=4))
