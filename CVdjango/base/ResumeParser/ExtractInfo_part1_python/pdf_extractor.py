import os
from .text_utils import extract_text_from_pdf, preprocess_text
from .NER_utils import initialize_stanford_ner,extract_persons_with_stanford_ner
from .regex_utils import extract_names_with_regular_expression, extract_emails, extract_phone_numbers, get_most_relevant_email,extract_publications

def process_pdfs(directory):
    """
    Main function to process all PDFs in a directory
    """
    all_data = []

    # Initialize Stanford NER
    st = initialize_stanford_ner()

    for filename in os.listdir(directory):
        if filename.endswith(".pdf"):

            # load pdf
            pdf_path = os.path.join(directory, filename)
            # Using text_utils to extract text from the PDF
            text = extract_text_from_pdf(pdf_path)

            # extract emails
            emails = extract_emails(text)
            # extract phone
            phone_numbers = extract_phone_numbers(text)
            # Store only the first phone number in the list
            first_phone_number = phone_numbers[0] if phone_numbers else None

            # preprocess the text
            preprocessed_text = preprocess_text(text)
            # extract names
            PersonFullName_with_regEx = extract_names_with_regular_expression(preprocessed_text)

            # if we don't have the name
            if PersonFullName_with_regEx:
                full_name_final = PersonFullName_with_regEx[0]
            else:
                # Extract persons and other entities using Stanford NER
                try:
                    persons_from_NER = extract_persons_with_stanford_ner(text, st)
                except Exception as error:
                    persons_from_NER = None
                # Extract the first person
                first_person_from_ner = persons_from_NER[0]['text']
                full_name_final = first_person_from_ner

            try:
                relevant_email = get_most_relevant_email(full_name_final, emails)
            except Exception as error:
                relevant_email = None

            try:
                # Extract publications using regex
                publications = extract_publications(preprocessed_text, full_name_final)

                # Create a list to store publication dictionaries
                publication_list = []

                # Iterate over the extracted publications and create dictionaries
                for publication in publications:
                    publication_dict = {
                        "title": publication,
                        "abstract": "",
                        "researchgate_url": "",
                        "googlescholar_url": "",
                        "year": "",
                        "embedding": ""
                    }
                    publication_list.append(publication_dict)
            except Exception as error:
                publication_list = None

            # Create a dictionary to store all the extracted data from PDF
            pdf_data = {
                "name": full_name_final,
                "email": relevant_email if relevant_email else "Unknown",
                "phone": first_phone_number if first_phone_number else "Unknown",
                "researchgate_url": '',
                "googlescholar_url": '',
                "publications": publication_list
            }

            all_data.append(pdf_data)

    return all_data

