
from ocr import PDFProcessor

def extract(file_path):
    processor = PDFProcessor(file_path)
    processor.process_pdf()
    processor.print_elements()
    return []
