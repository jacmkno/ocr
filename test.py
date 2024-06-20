
import generator
import extract

def test():
    # Generate the PDF and get the texts
    result = generator.generatePDF()
    generated_texts = result['texts']
    print("Generated Texts:", generated_texts)

    # Extract texts from the PDF
    extracted_texts = extract.extract(result['file_path'])

    # Compare the texts
    if generated_texts == extracted_texts:
        print("PASS")
    else:
        print("FAIL")

if __name__ == "__main__":
    test()
