import pdfplumber

def extract_text_from_pdf(pdf_path):
    text = ''
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text()
    return text

# pdf_path = './python/downloaded_file.pdf'
pdf_path = './python/건축물대장.pdf'
pdf_text = extract_text_from_pdf(pdf_path)
print(pdf_text)
