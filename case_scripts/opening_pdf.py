#/usr/bin/python3

# importing required modules 
import PyPDF2 
path= 'general-practice-tests-set1.pdf' 
path1= 'Citibank Account Statement-20130504 TO 20140503.pdf' 
# creating a pdf file object 
pdfFileObj = open(path1, 'rb')
output=open('output.txt','wb')
  
# creating a pdf reader object 
pdfReader = PyPDF2.PdfFileReader(pdfFileObj) 
  
# printing number of pages in pdf file 
print(pdfReader.numPages) 
  
# creating a page object 
pageObj = pdfReader.getPage(0) 
  
# extracting text from page 
print(pageObj.extractText()) 
  
# closing the pdf file object 
pdfFileObj.close() 
