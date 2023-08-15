# Define a class for the document structure
class Candidate:
    def __init__(self, name, age, email, phone,publicationpdf):
        self.name = name
        self.author = age
        self.phone = email
        self.publication = publication

class PublicationPDF:
    def __init__(self, title, researchgate_url='', googleScholar_url='',sematic_url=''):
        self.title = title
        self.researchgate_url = researchgate_url
        self.googleScholar_url = googleScholar_url
        self.sematic_url = sematic_url

class Publication:
    def __init__(self, url, title, year='', abstract='', citation='', topics='', type=''):
        self.url = url
        self.title = title
        self.year = year
        self.abstract = abstract
        self.citation = citation
        self.topics = topics
        self.type = type
class ResearchGate:
    def __init__(self, author_id, author_url, publications):
        self.author_id = author_id
        self.author_url = author_url
        self.publications = publications