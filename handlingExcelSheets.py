import openpyxl
wb = openpyxl.Workbook()
dir (wb)
sheet = wb.sheetnames('Sheet')
sheet['A1'] = 'Hello world!'
sheet['A1'].value
