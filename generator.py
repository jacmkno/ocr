
import pandas as pd
import numpy as np
from faker import Faker
import matplotlib.pyplot as plt
from fpdf import FPDF
from PIL import Image, ImageDraw, ImageFont

def generatePDF():
    # Initialize storage for texts
    texts = []

    # Generate random text using Faker
    fake = Faker()
    random_text = fake.paragraph(nb_sentences=5)
    texts.append(random_text)

    # Generate random table data
    data = {
        "Column 1": np.random.randint(1, 100, 10),
        "Column 2": np.random.randint(1, 100, 10),
        "Column 3": np.random.randint(1, 100, 10)
    }
    df = pd.DataFrame(data)

    # Add table texts
    for col in df.columns:
        texts.extend(df[col].astype(str).tolist())

    # Generate a random image (simple plot)
    plt.figure(figsize=(5, 3))
    plt.plot(np.random.randn(100).cumsum())
    plt.title("Random Plot")
    image_path = "random_plot.png"
    plt.savefig(image_path)
    plt.close()

    # Create images with text
    def create_image_with_text(text, image_path):
        # Create an image with white background
        img = Image.new('RGB', (200, 100), color=(255, 255, 255))
        d = ImageDraw.Draw(img)

        # Load a font
        font = ImageFont.load_default()

        # Add text to image
        d.text((10, 40), text, fill=(0, 0, 0), font=font)

        # Save the image
        img.save(image_path)
        texts.append(text)

    # Paths for images
    image_path1 = "image_with_text1.png"
    image_path2 = "image_with_text2.png"

    # Create images with text
    create_image_with_text("Sample Text 1", image_path1)
    create_image_with_text("Sample Text 2", image_path2)

    # Create a PDF
    pdf = FPDF()
    pdf.add_page()

    # Add random text
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, random_text)

    # Add a table
    pdf.set_font("Arial", size=10)
    pdf.ln(10)
    for i in range(len(df)):
        pdf.cell(40, 10, f"{df.iloc[i, 0]}", 1)
        pdf.cell(40, 10, f"{df.iloc[i, 1]}", 1)
        pdf.cell(40, 10, f"{df.iloc[i, 2]}", 1)
        pdf.ln(10)

    # Add images with text
    pdf.image(image_path, x=10, y=None, w=100)
    pdf.image(image_path1, x=10, y=None, w=100)
    pdf.image(image_path2, x=10, y=None, w=100)

    # Save the pdf
    file_path = "random_content_with_text_images.pdf"
    pdf.output(file_path)

    return {"file_path": file_path, "texts": texts}

# Run the function and display the output
if __name__ == "__main__":
    result = generatePDF()
    print(result)
