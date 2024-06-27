
from pdfocr import PDFProcessor

def extract(file_path, lang = None):
    processor = PDFProcessor(file_path)
    texts = processor.process_pdf(lang)
    return texts
