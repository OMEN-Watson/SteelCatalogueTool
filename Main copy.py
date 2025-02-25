import fitz  # PyMuPDF
filePathEqualUnequalAngles='equalUnequalAnglesCopy.pdf'

# Open the PDF file
pdf_document = "/mnt/data/equalUnequalAngles.pdf"
doc = fitz.open(filePathEqualUnequalAngles)

# Iterate through pages and extract text
for page_num in range(len(doc)):
    page = doc.load_page(page_num)
    text = page.get_text("text")  # You can use 'text', 'html', 'dict', etc.
    print(f"Page {page_num + 1} Text:\n", text)
