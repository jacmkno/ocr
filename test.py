import Levenshtein

def compare(generated_texts, extracted_texts):
    # Join the lists of texts into single strings
    generated_texts_str = ' '.join(generated_texts)
    extracted_texts_str = ' '.join(extracted_texts)

    # Perform the comparison using Levenshtein distance
    distance = Levenshtein.distance(generated_texts_str, extracted_texts_str)
    ratio = Levenshtein.ratio(generated_texts_str, extracted_texts_str) * 100
    opcodes = Levenshtein.opcodes(generated_texts_str, extracted_texts_str)

    # Calculate the number of additions, deletions, and substitutions
    additions = sum(1 for tag, i1, i2, j1, j2 in opcodes if tag == 'insert')
    deletions = sum(1 for tag, i1, i2, j1, j2 in opcodes if tag == 'delete')
    substitutions = sum(1 for tag, i1, i2, j1, j2 in opcodes if tag == 'replace')

    # Determine the result
    result = "PASS" if ratio == 100 else "FAIL"

    return result, ratio, additions, deletions, substitutions

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

    result, ratio, additions, deletions, substitutions = compare(generated_texts, extracted_texts)
    print(result)
    print(f"Ratio: {ratio}%")
    print(f"Deletions: {additions}%")
    print(f"Additions: {deletions}%")
    print(f"Substitutions: {substitutions}%")

if __name__ == "__main__":
    test()
