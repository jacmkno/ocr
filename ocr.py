
import fitz  # PyMuPDF
import pdfplumber
import pytesseract
from PIL import Image
import camelot

class PDFElement:
    def __init__(self, element_type, content, bbox, page_number):
        self.type = element_type
        self.content = content
        self.bbox = bbox
        self.page_number = page_number
    
    def __repr__(self):
        return f"Page {self.page_number}, Type: {self.type}, BBox: {self.bbox}\nContent: {self.content}\n"

class PDFProcessor:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path
        self.elements = []

    def upload_pdf():
        from google.colab import files
        uploaded = files.upload()
        for file_name in uploaded.keys():
            return PDFProcessor(file_name)

    def load_pdfs(self):
        self.pdf_document = fitz.open(self.pdf_path)
        self.pdf = pdfplumber.open(self.pdf_path)

    def close_pdfs(self):
        self.pdf.close()
        self.pdf_document.close()

    def classify_and_add_element(self, element_type, content, bbox, page_number):
        element = PDFElement(element_type, content, bbox, page_number)
        self.elements.append(element)

    def extract_text_blocks(self, page, page_number):
        for block in page.get_text("dict")["blocks"]:
            if "lines" in block:
                block_text = ""
                for line in block["lines"]:
                    for span in line["spans"]:
                        block_text += span["text"] + " "
                bbox = (block["bbox"][0], block["bbox"][1], block["bbox"][2], block["bbox"][3])
                self.classify_and_add_element('text', block_text.strip(), bbox, page_number)

    def extract_images(self, page, page_number):
        for img in page.images:
            img_bbox = (img['x0'], img['top'], img['x1'], img['bottom'])
            img_data = page.within_bbox(img_bbox).to_image(resolution=300).image
            img_content = pytesseract.image_to_string(Image.fromarray(img_data))
            self.classify_and_add_element('image', img_content, img_bbox, page_number)

    def extract_tables(self, page_number):
        tables = camelot.read_pdf(self.pdf_path, pages=str(page_number))
        for table in tables:
            table_bbox = (0, 0, 0, 0)  # Camelot does not provide bbox, default to (0,0,0,0)
            self.classify_and_add_element('table', table.df.to_json(), table_bbox, page_number)

    def process_page(self, page, page_number):
        page_elements = []

        # Extract text blocks
        self.extract_text_blocks(page, page_number)

        # Extract images
        self.extract_images(page, page_number)

        # Extract tables
        self.extract_tables(page_number)

    def process_pdf(self):
        self.load_pdfs()

        for page_number, page in enumerate(self.pdf.pages, start=1):
            pdf_page = self.pdf_document.load_page(page_number - 1)
            self.process_page(pdf_page, page_number)

        self.close_pdfs()

    def print_elements(self):
        for element in self.elements:
            print(element)
            print("-" * 80)
