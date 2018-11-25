#!/usr/bin/python3
from PyPDF2 import PdfFileReader, PdfFileWriter
input_path= 'Citibank Account Statement-20130504 TO 20140503.pdf'
output_path='nopasspdf2.pdf'
password='ARYA22SEP'
with open(input_path, 'rb') as input_file, \
   open(output_path, 'wb') as output_file:
   reader = PdfFileReader(input_file)
   reader.decrypt(password)
   

   writer = PdfFileWriter()

   for i in range(reader.getNumPages()):
     writer.addPage(reader.getPage(i))

   writer.write(output_file)

