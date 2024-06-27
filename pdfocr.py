import pdfplumber
import pytesseract
from PIL import Image
import io
import zlib

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
        self.lang = None

    def load_pdf(self):
        self.pdf = pdfplumber.open(self.pdf_path)

    def close_pdf(self):
        self.pdf.close()

    def classify_and_add_element(self, element_type, content, bbox, page_number):
        element = PDFElement(element_type, content, bbox, page_number)
        self.elements.append(element)

    def extract_text_blocks(self, page, page_number):
        for block in page.extract_words(use_text_flow=True, keep_blank_chars=True, y_tolerance=3):
            bbox = (block['x0'], block['top'], block['x1'], block['bottom'])
            self.classify_and_add_element('text', block['text'], bbox, page_number)

    def decodeImage(self, pdf_image):
        stream_data = pdf_image['stream'].get_data()
        filter_type = pdf_image['stream'].attrs['Filter'].name
        decode_params = pdf_image['stream'].attrs.get('DecodeParms')

        if filter_type == 'FlateDecode':
            try:
                decompressed_data = zlib.decompress(stream_data)
            except zlib.error:
                decompressed_data = zlib.decompress(stream_data, -15)  # Try decompressing with raw deflate

            if decode_params:
                predictor = decode_params.get('Predictor')
                if predictor == 15:
                    width = decode_params['Columns']
                    colors = decode_params['Colors']
                    bits_per_component = decode_params['BitsPerComponent']
                    row_size = (width * colors * bits_per_component + 7) // 8
                    decoded_data = bytearray()
                    for i in range(0, len(decompressed_data), row_size + 1):
                        filter_byte = decompressed_data[i]
                        if filter_byte == 0:  # No filter
                            decoded_data.extend(decompressed_data[i+1:i+1+row_size])
                        elif filter_byte == 2:  # Up filter
                            if i == 0:
                                decoded_data.extend(decompressed_data[i+1:i+1+row_size])
                            else:
                                for j in range(row_size):
                                    decoded_data.append((decompressed_data[i+1+j] + decoded_data[-row_size+j]) % 256)
                    decompressed_data = bytes(decoded_data)

            image = Image.frombytes('RGB', (pdf_image['stream'].attrs['Width'], pdf_image['stream'].attrs['Height']), decompressed_data)
        elif filter_type == 'DCTDecode':
            image = Image.open(io.BytesIO(stream_data))
        elif filter_type == 'JPXDecode':
            image = Image.open(io.BytesIO(stream_data))
        elif filter_type == 'CCITTFaxDecode':
            width, height = pdf_image['stream'].attrs['Width'], pdf_image['stream'].attrs['Height']
            image = Image.frombytes('1', (width, height), stream_data)
        else:
            raise ValueError(f"Unhandled filter: {filter_type}")
        
        return image

    def extract_images(self, page, page_number):
        P = page.bbox
        for img in page.images:
            img_bbox = (
                max(img["x0"], P[0]), 
                max(img["top"], P[1]), 
                min(img["x1"], P[2]), 
                min(img["bottom"], P[3])
            )
            cropped_image = page.within_bbox(img_bbox).to_image(resolution=600)
            img_pil = cropped_image.original
            img_content = pytesseract.image_to_string(img_pil, lang=self.lang)
            bbox = (img['x0'], img['top'], img['x1'], img['bottom'])
            self.classify_and_add_element('image', img_content, bbox, page_number)

    def process_page(self, page, page_number):
        self.extract_text_blocks(page, page_number)
        self.extract_images(page, page_number)

    def process_pdf(self, lang = None):
        self.load_pdf()
        if lang:
            langs = PDFProcessor.langs()
            if not lang in langs:
                print(langs)
                raise ValueError("Language Not supported: %s"%lang)
            self.lang = lang
        for page_number, page in enumerate(self.pdf.pages, start=1):
            print(f"Processing Page: {page_number}")
            self.process_page(page, page_number, )
            break
        self.close_pdf()

        # Return all extracted texts
        return [element.content.strip() for element in self.elements]

    def print_elements(self):
        for element in self.elements:
            print(element)
            print("-" * 80)
    
    def langs():
        import pycountry
        L = [(l, (lambda L: L.name if L else None)(pycountry.languages.get(alpha_3=l))) for l in pytesseract.get_languages(config='')]
        return dict([l for l in L if l[1]])