
# PDF Generator and Extractor

## Description

This project contains three main files:

1. **generator.py**: This script generates a PDF with random text, tables, and images. It has a function `generatePDF()` that returns the file path of the generated PDF and an array of the texts used to create the PDF.
2. **extract.py**: This script contains a function `extract(file_path)` that extracts texts from the PDF using OCR and returns them.
3. **test.py**: This script tests the functionality of `generator.py` and `extract.py`. It generates a PDF using `generator.py`, extracts texts from the generated PDF using `extract.py`, and checks if the extracted texts match the generated texts. The test prints "PASS" if the texts match and "FAIL" otherwise. It also prints the list of texts that were checked.

## How to Use

1. **Generate the PDF**:
    - Run `generator.py` to generate a PDF with random content.
    - The `generatePDF()` function will return the file path of the generated PDF and an array of the texts used.

2. **Extract Texts from PDF**:
    - Implement the `extract(file_path)` function in `extract.py` to extract texts from the PDF.
    - The function uses OCR to extract texts from the PDF and returns them.

3. **Run Tests**:
    - Run `test.py` to test the functionality of `generator.py` and `extract.py`.
    - The script will print the generated and extracted texts, the pass/fail status, and the percentage of matched texts.

## Example

```bash
python3 generator.py
python3 test.py
```

## Google Colab Requirements

To run this project on Google Colab, you need to install the following dependencies:

```bash
!pip install pymupdf pdfplumber pytesseract pillow camelot-py[cv]
!sudo apt-get install tesseract-ocr
!pip install google-colab
```

## Run in Chat GPT:

Attach the zip of the repo with this message: "Unzip this in your python environment and then run test.py and give me the output, bot stdout and stderr..." 

## Files

- `generator.py`
- `extract.py`
- `test.py`
- `ocr.py`
- `README.md`
