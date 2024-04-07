import os
import easyocr
from openai import OpenAI

OPENAI_API_KEY = os.getenv
openai_client = OpenAI(api_key=OPENAI_API_KEY)()
def extract_text_from_keyframes(keyframes_folder):
    extracted_texts = []
    
    # Create an OCR reader
    reader = easyocr.Reader(['en'])  # Initialize with English language
    
    # Iterate through keyframes folder
    for filename in os.listdir(keyframes_folder):
        if filename.endswith(".jpg"):
            # Load image using OpenCV
            image_path = os.path.join(keyframes_folder, filename)
            
            # Perform OCR using easyocr
            result = reader.readtext(image_path)
            
            # Extract text from OCR result
            extracted_text = ""
            for detection in result:
                extracted_text += detection[1] + " "  # Concatenate text from each detection
            
            # Append extracted text to the list
            extracted_texts.append(extracted_text)
    
    return extracted_texts

# Example usage:
keyframes_folder = "final_keyframes"  # Change this to your keyframes folder
extracted_texts = extract_text_from_keyframes(keyframes_folder)

# Print extracted texts
for i, text in enumerate(extracted_texts):
    print(f"Keyframe {i+1} text:\n{text}\n")


def generate_pdf_notes(extracted_text):
    # Construct input prompt
    prompt = f"Act as a PDF notes generator and create a proper PDF with good formatting based on the following text:\n{extracted_text}"

    # Call OpenAI API to generate PDF notes
    response = openai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    # Process output
    pdf_content = response.choices[0].text.strip()

    # Save PDF
    with open("notes.pdf", "wb") as f:
        f.write(pdf_content.encode('utf-8'))

    print("PDF notes generated successfully.")
    
    return response.choices[0].message.content

# Example usage:
extracted_text = extracted_texts
generate_pdf_notes(extracted_text)