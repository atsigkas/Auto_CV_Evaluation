import os
from nltk.tag import StanfordNERTagger

# Function to initialize the Stanford NER tagger
def initialize_stanford_ner():
    # Set the paths to the Stanford NER model and jar files
    stanford_ner_model = 'C:/Users/atsigkas/AUTO_CV/Auto_CV_Evaluation/stanford-ner-4.2.0/stanford-ner-2020-11-17/classifiers/english.all.3class.distsim.crf.ser.gz'
    stanford_ner_jar = 'C:/Users/atsigkas/AUTO_CV/Auto_CV_Evaluation/stanford-ner-4.2.0/stanford-ner-2020-11-17/stanford-ner.jar'

    # Set the environment variable for the Java runtime (replace 'java_path' with your Java installation path)
    java_path = '/path/to/java/bin/java'
    os.environ['JAVAHOME'] = java_path

    # Initialize the Stanford NER tagger
    st = StanfordNERTagger(stanford_ner_model, stanford_ner_jar)
    return st

# Function to perform named entity recognition using Stanford NER
def stanford_ner(text, st):
    # Tokenize the text
    tokens = text.split()

    # Perform named entity recognition
    tags = st.tag(tokens)

    # Create a list to store the named entities
    named_entities = []

    # Extract named entities
    current_entity = None
    for word, tag in tags:
        if tag != 'O':
            if current_entity is None:
                current_entity = {'type': tag, 'text': word}
            else:
                current_entity['text'] += ' ' + word
        else:
            if current_entity is not None:
                named_entities.append(current_entity)
                current_entity = None

    return named_entities

    
def extract_persons_with_stanford_ner(text, st):
    stanford_ner_result = stanford_ner(text, st)
    persons = [entity for entity in stanford_ner_result if entity['type'] == 'PERSON']
    return persons

# Function to extract all named entities other than persons found by Stanford NER
def extract_other_entities_with_stanford_ner(text, st):
    stanford_ner_result = stanford_ner(text, st)
    other_entities = [entity for entity in stanford_ner_result if entity['type'] != 'PERSON']
    return other_entities
