import PyPDF2

name = "pdf/m.pdf"

# Open the PDF file in read-binary mode
with open(name, "rb") as pdf_file:
    # Create a PDF reader object
    reader = PyPDF2.PdfReader (pdf_file)
    
    # Extract the text from each page of the PDF
    text = ""
    for page_num in range(23, 26):
        page = reader.pages[page_num]
        text += page.extract_text()

print(text)