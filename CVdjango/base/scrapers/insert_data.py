from CVdjango.base.db.utils import *

title="Fully automated identification of skin morphology in raster‐scan optoacoustic mesoscopy using artificial intelligence"
candidate = {
                "author": "Serafeim Moustakidis",
                "email": "a@a.gr",
                "phone": "53453",
                "researchgate_url": '',
                "googlescholar_url": '',
                "sematic_url": '',
                "publication": [
                    {
                        "title": title,
                        "researchgate_url": '',
                        "googlescholar_url": '',
                        "sematic_url": ''
                    }
                ],
                "researchgate": [],
                "googlescholar": []
            }
mongo_handler = MongoDBHandler("localhost", 27017)
client = mongo_handler.connect()
db, col = mongo_handler.get_database_and_collection('CVproject', 'Candinates')
mongo_handler.insert_one_document(col,candidate)