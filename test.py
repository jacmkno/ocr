from fuzzywuzzy import fuzz

def compare(generated_texts, extracted_texts):
    # Join the lists of texts into single strings
    generated_texts_str = ' '.join(generated_texts)
    extracted_texts_str = ' '.join(extracted_texts)

    # Perform the comparison using fuzzywuzzy
    ratio = fuzz.ratio(generated_texts_str, extracted_texts_str)
    partial_ratio = fuzz.partial_ratio(generated_texts_str, extracted_texts_str)
    token_sort_ratio = fuzz.token_sort_ratio(generated_texts_str, extracted_texts_str)
    token_set_ratio = fuzz.token_set_ratio(generated_texts_str, extracted_texts_str)

    if ratio == 100:
        result = "PASS"
    else:
        result = "FAIL"

    return result, ratio, partial_ratio, token_sort_ratio, token_set_ratio

import generator
import extract

def test():
    # Generate the PDF and get the texts
    result = generator.generatePDF()
    generated_texts = result['texts']
    print("Generated Texts:", generated_texts)

    # Extract texts from the PDF
    extracted_texts = extract.extract(result['file_path'])
    print("Extracted Texts:", extracted_texts)

    result, ratio, partial_ratio, token_sort_ratio, token_set_ratio = compare(generated_texts, extracted_texts)
    print(result)
    print(f"Ratio: {ratio}%")
    print(f"Partial Ratio: {partial_ratio}%")
    print(f"Token Sort Ratio: {token_sort_ratio}%")
    print(f"Token Set Ratio: {token_set_ratio}%")

if __name__ == "__main__":
    test()
