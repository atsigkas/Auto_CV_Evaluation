from scholarly import scholarly
import json
from CVdjango.base.scrapers.scholar_api import *


# search by unique author id
author_id = 'kJBcnigAAAAJ'
author = scholarly.search_author_id(author_id)

# fill author including their publications
author_filled = scholarly.fill(author, sections=[ 'publications'])

# print the filled author information

# get author's publications

for pub in author_filled['publications']:
    try:
        print(pub["bib"]["title"])
        print(json.dumps(pub, indent=4))
        #print(json.dumps(pub_filled, indent=4))
        break
    except KeyError:
        print("Abstract not available.")
    print()

'''
############the least things so to get results
{
        "container_type": "Publication",
        "source": "AUTHOR_PUBLICATION_ENTRY",
        "author_pub_id": "kJBcnigAAAAJ:W7OEmFMy1HYC",
        "bib": {
            "title":""
        }
    }
############ After Fill
{
    "container_type": "Publication",
    "source": "AUTHOR_PUBLICATION_ENTRY",
    "bib": {
        "title": "Application of artificial neural networks for natural gas consumption forecasting",
        "pub_year": 2020,
        "citation": "Sustainability 12 (16), 6409, 2020",
        "author": "Athanasios Anagnostis and Elpiniki Papageorgiou and Dionysis Bochtis",
        "journal": "Sustainability",
        "volume": "12",
        "number": "16",
        "pages": "6409",
        "publisher": "MDPI",
        "abstract": "The present research study explores three types of neural network approaches for forecasting natural gas consumption in fifteen cities throughout Greece; a simple perceptron artificial neural network (ANN), a state-of-the-art Long Short-Term Memory (LSTM), and the proposed deep neural network (DNN). In this research paper, a DNN implementation is proposed where variables related to social aspects are introduced as inputs. These qualitative factors along with a deeper, more complex architecture are utilized for improving the forecasting ability of the proposed approach. A comparative analysis is conducted between the proposed DNN, the simple ANN, and the advantageous LSTM, with the results offering a deeper understanding the characteristics of Greek cities and the habitual patterns of their residents. The proposed implementation shows efficacy on forecasting daily values of energy consumption for up to four years. For the evaluation of the proposed approach, a real-life dataset for natural gas prediction was used. A detailed discussion is provided on the performance of the implemented approaches, the ANN and the LSTM, that are characterized as particularly accurate and effective in the literature, and the proposed DNN with the inclusion of the qualitative variables that govern human behavior, which outperforms them."
    },
    "filled": true,
    "author_pub_id": "kJBcnigAAAAJ:Y0pCki6q_DkC",
    "num_citations": 34,
    "citedby_url": "/scholar?hl=en&cites=13323191008473362529",
    "cites_id": [
        "13323191008473362529"
    ],
    "pub_url": "https://www.mdpi.com/2071-1050/12/16/6409",
    "url_related_articles": "/scholar?oi=bibs&hl=en&q=related:YbC7BqJ75bgJ:scholar.google.com/",
    "cites_per_year": {
        "2020": 2,
        "2021": 11,
        "2022": 14,
        "2023": 7
    }
    
############ Before Fill
{
    "container_type": "Publication",
    "source": "AUTHOR_PUBLICATION_ENTRY",
    "bib": {
        "title": "Bone metastasis classification using whole body images from prostate cancer patients based on convolutional neural networks application",
        "pub_year": "2020",
        "citation": "PloS one 15 (8), e0237213, 2020"
    },
    "filled": false,
    "author_pub_id": "kJBcnigAAAAJ:W7OEmFMy1HYC",
    "num_citations": 58,
    "citedby_url": "https://scholar.google.com/scholar?oi=bibs&hl=en&cites=3321677359618938670",
    "cites_id": [
        "3321677359618938670"
    ]
}
'''


