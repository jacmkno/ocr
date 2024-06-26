
from pdfocr import PDFProcessor

def extract(file_path):
    processor = PDFProcessor(file_path)
    texts = processor.process_pdf()
    return texts
