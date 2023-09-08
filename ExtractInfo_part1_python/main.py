import os
import json
from text_utils import extract_text_from_pdf, preprocess_text, clean_text_for_phone_extraction, remove_unrecognized_unicode
from NER_utils import initialize_stanford_ner,extract_persons_with_stanford_ner, extract_other_entities_with_stanford_ner
from regex_utils import extract_names_with_regular_expression, extract_emails, extract_phone_numbers, get_most_relevant_email,extract_publications


# Main function to process all PDFs in a directory
def process_pdfs(directory):
    all_data = []

    # Initialize Stanford NER tagger
    st = initialize_stanford_ner()

    for filename in os.listdir(directory):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(directory, filename)

            # Using text_utils to extract text from the PDF
            text = extract_text_from_pdf(pdf_path)

            # Using regular expression to extract emails
            emails = extract_emails(text)

            # Using text_utils to preprocess the text
            preprocessed_text = preprocess_text(text)
            
            # Clean the text for phone extraction
            # cleaned_text = remove_unrecognized_unicode(preprocessed_text)

            # Using regular expression to extract phone numbers from the cleaned text
            phone_numbers = extract_phone_numbers(text)

            # Store only the first phone number in the list
            first_phone_number = phone_numbers[0] if phone_numbers else None
            
            # Using regular expression to extract names
            PersonFullname_with_regEx = extract_names_with_regular_expression(preprocessed_text)
            
            if not PersonFullname_with_regEx:
                persons_from_NER = extract_persons_with_stanford_ner(text,st)
                
                # Extract the first person
                first_person_from_NER = persons_from_NER[0]['text'] if persons_from_NER else None
                
                full_NAME_Final =first_person_from_NER
            else:
                full_NAME_Final=PersonFullname_with_regEx[0]
                
            
            # Extract persons and other entities using Stanford NER
            #persons_from_NER = extract_persons_with_stanford_ner(text, st)

            # Get the most relevant email for the file
            relevant_email = get_most_relevant_email(full_NAME_Final, emails)

            # Extract publications using regex
            publications = extract_publications(preprocessed_text,full_NAME_Final)

            # Create a dictionary to store all the extracted data for each PDF
            pdf_data = {
                "filename": filename,
                #"text": text,  # Add the text
                "preprocessed_text": preprocessed_text,  # Add the text
                "fullName": full_NAME_Final,
                "email": relevant_email,
                "phoneNumber": first_phone_number,
                "publications' titles": publications
            }

            all_data.append(pdf_data)

    return all_data

if __name__ == "__main__":
    directory = "C:/Users/atsigkas/AUTO_CV/MOCK CV Data"
    # Process PDFs in the directory
    all_data = process_pdfs(directory)

    # Save the data to a JSON file
    with open("extracted_data.json", "w") as json_file:
        json.dump(all_data, json_file, indent=4)

    # Print all the extracted information for each PDF
    for data in all_data:
        print("____________")
        print(f"File: {data['filename']}")
        print("Emails extracted using regular expression:")
        print(data["email"])
        print("Phone numbers extracted using regular expression:")
        print(data["phoneNumber"])
        print("Publications extracted using regex:")
        print(data["publications' titles"])  # Print extracted publications
        print("First person extracted using Stanford NER:")
        if data["fullName"]:
            print(data["fullName"])
        else:
            print("No persons found.")
        print("____________")


