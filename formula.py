import openpyxl

# Path to your Excel file (adjust the path if needed)
path = 'C:/PyTask/ExcelSheets/Apple-model-dummy (1).xlsx'
  

# Load the workbook with data_only=False to get formulas
wb_formulas = openpyxl.load_workbook(path, data_only=False)
ws_formulas = wb_formulas.active

# Load the workbook with data_only=True to get calculated values
wb_values = openpyxl.load_workbook(path, data_only=True)
ws_values = wb_values.active

# Check for formulas in columns B and D
for row in ws_formulas.iter_rows(min_row=1, max_row=ws_formulas.max_row):
    for cell in row:
        # Skip merged cells
        if isinstance(cell, openpyxl.cell.MergedCell):
            continue
        
        if cell.column_letter in ['B']:  # Check columns B and D
            formula = cell.value if isinstance(cell.value, str) and cell.value.startswith('=') else "No formula"
            value = ws_values[cell.coordinate].value
            
            # Print formula and value
            print(f"{formula}")
