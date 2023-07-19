from CVdjango.base.db.utils import *

candidate = {
                "author": "Athanasios Anagnostis",
                "email": "a@a.gr",
                "phone": "53453",
                "researchgate_url": '',
                "googlescholar_url": '',
                "sematic_url": '',
                "publication": [
                    {
                        "title":'Smart Technologies for Sustainable Water Management: An Urban Analysis',
                        "researchgate_url": '',
                        "googleScholar_url": '',
                        "sematic_url": ''
                    }
                ],
                "researchgate": []
            }
mongo_handler = MongoDBHandler("localhost", 27017)
client = mongo_handler.connect()
db, col = mongo_handler.get_database_and_collection('CVproject', 'Candinates')
mongo_handler.insert_one_document(col,candidate)