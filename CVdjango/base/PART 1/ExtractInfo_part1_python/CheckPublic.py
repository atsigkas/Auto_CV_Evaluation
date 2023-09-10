import re

def extract_publications(text, surname):
    # Construct the regex pattern with the surname constraint
    #Pavlopoulos.*?\"(.*?)\".*?\(\d{4}\)
    #regex_pattern = rf'{re.escape(surname)}.{0,250}?\"(.*?)\".*?\(\d{4}\)'
   #regex_pattern = rf'{re.escape(surname)}.{0,250}?\"(.*?)\".*?\(\d{{4}}\)'
    regex_pattern = rf'{re.escape(surname)}.{{0,250}}?\"(.*?)\".*?\(\d{{4}}\)'

    publications = []
    matches = re.findall(regex_pattern, text)
    publications.extend(matches)
    return publications


text = 'EXTENSIVE CURRICULUM VITAE IOANNIS Pavlopoulos,EXTENSIVE CURRICULUM VITAEEXTENSIVE CURRICULUM VITAEEXTENSIVE CURRICULUM VITAEEXTENSIVE CURRICULUM VITAEEXTENSIVE CURRICULUM VITAEEXTENSIVE CURRICULUM VITAEEXTENSIVE CURRICULUM VITAEEXTENSIVE CURRICULUM VITAEEXTENSIVE CURRICULUM VITAEEXTENSIVE CURRICULUM VITAEEXTENSIVE CURRICULUM VITAEEXTENSIVE CURRICULUM VITAE I., Westerski, A. \"Building Consensus via a Semantic Web Collaborative Space.\" (2022) Pavlopoulos'
# Call the extract_publications function
candidate_name = 'IOANNIS PAvlopoulos'
name_parts = candidate_name.split()
surname = name_parts[-1].lower().capitalize()
print(surname)
publications = extract_publications(text,surname)


# Print the extracted publications
for i, publication in enumerate(publications, start=1):
    print(f"{i}. {publication}")
    print('-----')
    
