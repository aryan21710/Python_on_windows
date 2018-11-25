import re
from openpyxl import Workbook

book = Workbook()
sheet = book.active
expr='(.*),(.*),(.*)'
cnt=0;
transaction=[];
x=[];
with open('sample.xlsx') as f1:
     for line in f1:
         cnt+=1;
         line=line.rstrip();
         reMatch=re.search('(.*),(.*),(.*)',line)
         if (reMatch):
               #print ('DATE:-',reMatch.group(1), ',TRANSACTION:-', reMatch.group(2), ', AMOUNT:-',reMatch.group(3))
             #print ('groups:-',reMatch.groups());
             x=list(reMatch.groups());
             #x.append(''.join(reMatch.groups()));
             #print ('x:-',x)
         transaction.append(x);
#print (transaction)
#print ('THE BANK TRANSACTION LIST:-',transaction);
for x in range(cnt):
    for y in range(3):
          sheet.cell(row=x+1, column=y+1).value=transaction[x][y]

book.save("citi_python.xlsx")
