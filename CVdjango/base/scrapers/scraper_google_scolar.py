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


def fetch_data():

    author = 'Stravros Solakis'
    papers = ['A Comparative Analysis of Machine Learning Algorithms for Sentiment Analysis',
              'Emerging Trends in Cybersecurity Threats and Countermeasures']
    email ='ssolakis@email.com'
    phone ='3453543354'
    # Search in Database
    mongo_handler = utils.MongoDBHandler("localhost", 27017)
    client = mongo_handler.connect()

    if client:
        db, col = mongo_handler.get_database_and_collection('CVproject', 'Candinates')
        #ok = mongo_handler.insert_one_document(col)
        '''
        TODO
        similar way when seaching the google with the name
        '''
        profiles = mongo_handler.find_document(col, author)
        print(f"Find : {profiles}")

        found = False
        '''
        check email
        check number
        check papers
        try and exeption
        '''
        for profile in profiles:
            print(profile['Author'])
            if profile['email']==email or profile['phone']==phone:
                found=True
                break
            if found is True:
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
            Google search
            populate the database 
            '''

    else:
        print("Client stance is invalid")


    '''
    try :
        # Retrieve the author's data, fill-in, and print
        search_query = scholarly.search_author(name)
        author = scholarly.fill(next(search_query))
        scholarly.pprint(scholarly.fill(author, sections=['Publications']))
    except Exception as error:
        return None
        
    # Insert In Database
    mongo_handler = utils.MongoDBHandler("localhost", 27017)
    client = mongo_handler.connect()

    if client:
        db, col = mongo_handler.get_database_and_collection('CVproject', 'Candinates')
        document = mongo_handler.insert_one_document(col)
        print("Insert Done")
    else:
        print("Client stance is invalid")
    '''

