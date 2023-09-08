import re
from difflib import SequenceMatcher

import re

def extract_names_with_regular_expression(text):
    # Match "Full Name" followed by two words starting with capitals
    full_name_pattern = r'\bFull Name\b.*?([A-Z][a-z]+ [A-Z][a-z]+)'
    matches = re.findall(full_name_pattern, text, flags=re.IGNORECASE)
    
    # Extract the matched names
    names = [match.strip() for match in matches]
    
    return names


def extract_emails(text):
    emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
    return emails

def extract_phone_numbers(text):
    # Regular expressions for different phone number formats
    # The patterns below cover various formats including local, international, and common separators like "-", ".", or " ".
    phone_patterns = [
        r'\b\d{2,4}[-.\s]\d{2,4}[-.\s]\d{3,4}\b',  # Format: XX-XX-XXX or XXXX-XXXX-XXX
        r'\b\d{3}[-.\s]\d{3}[-.\s]\d{4}\b',  # Format: XXX-XXX-XXXX
        r'\b\d{2}[-.\s]\d{3}[-.\s]\d{2}[-.\s]\d{2}\b',  # Format: XX-XXX-XX-XX
        r'\+\d{2}\s?\d{10}\b',  # Format: +30 6543434321
        r'\+\(\d{2}\)\s?\d{10}\b',  # Format: (+30) 6934342345
        r'\+\(\d{2}\)\d{10}\b',  # Format: (+30)5555555555
        r'\+\(\d{2}\)\s?\d{9}\b',  # Format: (+30) 555555555
        r'\+\d{3}\d{9}\b',  # Format: +305434345434
        r'\+\d{2}\s?\d{9}\b',  # Format: +30 5456345436
        r'\+\d{2}[-]\d{9}\b',  # Format: +30-4345434345
        r'\b\d{9,15}\b',  # Format: 4311232123
        r'\+\d{1}\s?\(\d{3}\)\s?\d{3}[-.\s]\d{4}\b',  # Format: +1 (555) 123-4567
    ]

    # Combine all patterns using "|"
    combined_pattern = '|'.join(phone_patterns)

    phone_numbers = re.findall(combined_pattern, text)
    return phone_numbers



def is_similar_email(str1, str2, threshold=0.8):
    # Split the email addresses at the "@" symbol and compare the part before "@" for similarity
    email1_username = str1.split("@")[0]
    email2_username = str2.split("@")[0]

    similarity_ratio = SequenceMatcher(None, email1_username, email2_username).ratio()
    return similarity_ratio >= threshold

def get_most_relevant_email(first_person, emails):
    relevant_email = None

    for email in emails:
        if is_similar_email(email, first_person):
            relevant_email = email
            break

    if not relevant_email:
        # If no similar email is found, return the first email in the list
        relevant_email = emails[0]

    return relevant_email

# Function to extract publications using regex patterns
def extract_publications(text, candidate_name):
    # Extract the surname from the candidate's name
    name_parts = candidate_name.split()
    surname = name_parts[-1].lower().capitalize()
    print(surname)
    
    # Add the publication regex patterns
    regex_patterns = [
        # MLA cititation for i) publications in Journals AND ii) publication in Conferences wih Review
        # ENA GENIKO KALO FORMAT EINAI :
        # 1. \"(.*?)\".*?\(\d{4}\)
        # TO KALO akoma kalo pou vazei mesa kai quotes se periergi morfi einai 
        # 2. r'[\"“”](.*?)[\"“”].*?\(\d{4}\)', 
        # 3. Prepei na apofasisoume an protimame to 3 i ta 1 i 2--- MAKE IT WORK cause its more robust approach
        # Pavlopoulos.*?\"(.*?)\".*?\(\d{4}\)
        rf'{re.escape(surname)}.{{0,250}}?\"(.*?)\".*?\(\d{{4}}\)'
    ]
    publications = []
    for pattern in regex_patterns:
        matches = re.findall(pattern, text)
        publications.extend(matches)
    return publications
