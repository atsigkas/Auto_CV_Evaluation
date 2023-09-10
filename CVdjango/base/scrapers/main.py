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
    '''
    fdfsdf

    '''