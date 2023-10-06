import re
import pdfplumber
import unicodedata

def extract_text_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        # Extract text from all pages and concatenate
        text = "\n".join([page.extract_text() for page in pdf.pages])
    return text

def preprocess_text(text):
    # Replace left double quotes ("\u201C") with regular double quotes (""")
    text = text.replace('\u201C', '"')
    
    # Replace right double quotes ("\u201C") with regular double quotes (""")
    text = text.replace('\u201d', '"')
    
    # Remove special characters except for hyphen and apostrophe
    text = re.sub(r'[^\w\s\'"\-,.:/)(]', ' ', text)
    
    # Remove Greek and non-English characters using a regular expression
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)

    # Replace multiple spaces with a single space
    text = re.sub(r'\s+', ' ', text)

    # Remove leading and trailing spaces
    text = text.strip()

    # Replace newline characters with spaces
    text = text.replace('\n', ' ')

    return text

def clean_text_for_phone_extraction(text):
    # Replace spaces with a special character '@'
    cleaned_text = re.sub(r'\s', ' ', text)
    # Keep only the specified symbols, numbers, and '@' character
    cleaned_text = re.sub(r'[^\d()+\-, ]', '', cleaned_text)
    return cleaned_text

def remove_unrecognized_unicode(text):
    # Define the range of recognized Unicode characters you want to keep
    recognized_range = (0, 127)  # ASCII characters (0 to 127) are usually recognized

    cleaned_text = ""

    for char in text:
        char_code = ord(char)
        if recognized_range[0] <= char_code <= recognized_range[1]:
            cleaned_text += char
        elif unicodedata.category(char).startswith("P"):  # Keep punctuation characters
            cleaned_text += char

    return cleaned_text

