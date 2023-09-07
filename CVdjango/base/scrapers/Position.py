from ..db import utils
from CVdjango.base.ML.Embedding.embedding import *

def insert_position(positon):
    # Search in Database
    mongo_handler = utils.MongoDBHandler("localhost", 27017)
    client = mongo_handler.connect()
    db, col = mongo_handler.get_database_and_collection('CVproject', 'Positionss')
    col.insert_one(positon)

po={
        'title': 'BERT',
        'abstract': 'We introduce a new language representation model called BERT'
}
insert_position(po)

class Position:
    def __init__(self, title="", abstract=""):
        self.title = title
        self.abstract = abstract

    def __repr__(self):
        return f"Position(title='{self.title}', abstract='{self.abstract}')"

