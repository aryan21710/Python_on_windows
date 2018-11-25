#!/usr/bin/python3
import docx2txt
'''
input_path='nopasspdf2.docx'
output_path='doctopdf2.pdf'
with open(input_path, 'rb') as input_file, \
   open(output_path, 'w') as output_file:
   text = docx2txt.process("nopasspdf2.docx")
   #print (text)
   output_file.write(text) 
import PyPDF2
pdfFileObj = open('nopasspdf2.docx', 'rb')
pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
print('NO OF PAGES:-',pdfReader.numPages)

pageObj = pdfReader.getPage(0)
print (pageObj.extractText())   
'''
from fpdf import FPDF

text = docx2txt.process("nopasspdf2.docx")
pdf = FPDF()
pdf.add_page()
pdf.set_xy(0, 0)
pdf.set_font('arial', 'B', 13.0)
pdf.cell(ln=0, h=5.0, align='L', w=0, txt=text, border=0)
pdf.output('test.pdf', 'F')
