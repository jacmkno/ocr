
import generator
import extract

def test():
    # Generate the PDF and get the texts
    result = generator.generatePDF()
    generated_texts = result['texts']
    print("Generated Texts:", generated_texts)

    # Extract texts from the PDF
    extracted_texts = extract.extract(result['file_path'])

    # Calculate the percentage of matched texts
    matched_texts = [text for text in generated_texts if text in extracted_texts]
    total_texts = len(generated_texts)
    matched_percentage = (len(matched_texts) / total_texts) * 100 if total_texts > 0 else 0

    # Compare the texts
    if generated_texts == extracted_texts:
        print("PASS")
    else:
        print("FAIL")

    print(f"Matched Texts: {len(matched_texts)}/{total_texts}")
    print(f"Matched Percentage: {matched_percentage:.2f}%")

if __name__ == "__main__":
    test()
