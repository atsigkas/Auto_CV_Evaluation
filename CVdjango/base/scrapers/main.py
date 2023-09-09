import pprint
from scholarly import scholarly, ProxyGenerator
from ..db import utils
from difflib import SequenceMatcher


def proxy():
    pg = ProxyGenerator()
    success = pg.FreeProxies()
    scholarly.use_proxy(pg)


def similarity(a, b):
    return SequenceMatcher(None, a, b).ratio()

#title="SVM-based fuzzy decision trees for classification of high spatial resolution remote sensing images"
#title2="Right Ventricular Volume Prediction by Feature Tokenizer Transformer-Based Regression of 2D Echocardiography Small-Scale Tabular Data"
title='Uncovering the Black Box of Coronary Artery Disease Diagnosis: The Significance of Explainability in Predictive Models'
title2='Classification models for assessing coronary artery disease instances using clinical and biometric data: an explainable man-in-the-loop approach'
candidate = {
                "author": "Elpiniki I Papageorgiou",
                "email": "a@a.gr",
                "phone": "53453",
                "researchgate_url": '',
                "googlescholar_url": '',
                "sematic_url": '',
                "publication": [
                    {
                        "title": title,
                        "abstract":'',
                        "researchgate_url": '',
                        "googlescholar_url": '',
                        "sematic_url": '',
                    },
                    {
                        "title": title2,
                        "abstract":'',
                        "researchgate_url": '',
                        "googlescholar_url": '',
                        "sematic_url": '',
                        "embedding" : ''
                    }
                ]
            }

def fetch_data():

    # Search in Database
    mongo_handler = utils.MongoDBHandler("localhost", 27017)
    client = mongo_handler.connect()

    if client:
        db, col = mongo_handler.get_database_and_collection('CVproject', 'Candinates')
        profiles = mongo_handler.find_document_one(col, "author",candidate["author"])
        print(f"Find : {profiles}")

        found = False
        '''
        check email
        check number
        check papers
        try and exception
        '''

        print(profile['Author'])
        if profile['email']==email or profile['phone']==phone:
            found=True
            break
        print(profile['Author'])
        for publication in profile['Publications']:
            if found is True:
                break
        for paper in papers:
            if similarity(publication['title'], paper) > 0.9:
                print(f'Found the paper,so the Profile exist')
                found = True
                break
        if found is False:
            '''
            Insert after the PDF
            run each procedure
            '''
        else:
            '''
                Check after if it is empty
                researchgate_url
                googleScholar_url
                sematic_url
                then run each procedure
            '''
        '''
        In this point we have all the information  for the Candidate
        
        '''