# import fitz  # PyMuPDF

# def extract_text(pdf_file):
#     text = ""
#     pdf_document = fitz.open(pdf_file)
#     for page_num in range(len(pdf_document)):
#         page = pdf_document.load_page(page_num)
#         text += page.get_text()
#     return text


import PyPDF2


def extract_text(uploaded_file):
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    num_pages = len(pdf_reader.pages)
    text = ""
    for page_num in range(num_pages):
        page = pdf_reader.pages[page_num]
        text += page.extract_text()
    return text
