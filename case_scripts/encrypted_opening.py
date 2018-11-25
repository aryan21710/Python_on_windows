#/usr/bin/python3

from PyPDF2 import PdfFileReader, PdfFileWriter
path1= 'Citibank Account Statement-20130504 TO 20140503.pdf' 
  

f = PdfFileReader(path1, "rb")
output = PdfFileWriter()
f.decrypt ('ARYA22SEP')

# Copy the pages in the encrypted pdf to unencrypted pdf with name noPassPDF.pdf
for pageNumber in range (0, f.getNumPages()):
   output.addPage(f.getPage(pageNumber))
   # write "output" to noPassPDF.pdf
   outputStream = file("noPassPDF.pdf", "wb")
   output.write(outputStream)
   outputStream.close()
'''
#Open the file now
   if sys.platform.startswith('darwin'):#open in MAC OX
       subprocess.call(["open", "noPassPDF.pdf"])
'''
