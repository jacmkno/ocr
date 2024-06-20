
# PDF Generator and Extractor

## Description

This project contains three main files:

1. **generator.py**: This script generates a PDF with random text, tables, and images. It has a function `generatePDF()` that returns the file path of the generated PDF and an array of the texts used to create the PDF.
2. **extract.py**: This script contains a placeholder function `extract(file_path)` that currently returns an empty array. This function is intended to extract texts from the PDF.
3. **test.py**: This script tests the functionality of `generator.py` and `extract.py`. It generates a PDF using `generator.py`, extracts texts from the generated PDF using `extract.py`, and checks if the extracted texts match the generated texts. The test prints "PASS" if the texts match and "FAIL" otherwise. It also prints the list of texts that were checked.

## How to Use

1. **Generate the PDF**:
    - Run `generator.py` to generate a PDF with random content.
    - The `generatePDF()` function will return the file path of the generated PDF and an array of the texts used.

2. **Extract Texts from PDF**:
    - Implement the `extract(file_path)` function in `extract.py` to extract texts from the PDF.
    - Currently, the function returns an empty array.

3. **Run Tests**:
    - Run `test.py` to test the functionality of `generator.py` and `extract.py`.
    - The script will print "PASS" if the texts match and "FAIL" otherwise. It will also print the list of texts that were checked.

## Example

```bash
python3 generator.py
python3 test.py
```

## Files

- `generator.py`
- `extract.py`
- `test.py`
- `README.md`
