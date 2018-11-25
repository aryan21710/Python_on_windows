import re
from openpyxl import Workbook

book = Workbook()
sheet = book.active
expr='([a-zA-Z0-9\s]*),'
expr1=',\s*([0-9]*)'
cnt=0;
transaction=[];
with open('sample_bank_stat.xlsx') as f1:
     for line in f1:
         cnt+=1;
         line=line.rstrip();
         date=re.findall(expr,line);
         if (date):
            print(date,' FOR LINE:-' , line);
            output1=re.findall(expr1,line)
            if (output1):
               print(output1,' FOR LINE:-' , line);
               date.append(output1[1]);
               print ('DATE:-',date[0], ',TRANSACTION:-', date[1], ', AMOUNT:-',date[2]);
            transaction.append(date);
print (transaction);
print ('THE BANK TRANSACTION LIST:-',transaction);
for x in range(cnt):
    for y in range(3):
          sheet.cell(row=x+1, column=y+1).value=transaction[x][y]

book.save("sample2.xlsx")
