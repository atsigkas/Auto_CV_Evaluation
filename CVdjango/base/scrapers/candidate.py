class Candidate:
    def __init__(self, data=None):
        self.candidate = {}
        if data:
            self.override_data(data)

    def override_data(self, new_data):
        self.candidate.update(new_data)

    def insert_candidate(self, col):
        col.insert_one(self.candidate)

    def update_candidate(self, col):
        col.update_one(
            {"_id": self.candidate['_id']},
            {"$set": {
                "publication": self.candidate['publication'],
                "researchgate": self.candidate.get('researchgate', []),
                "googlescholar": self.candidate.get('googlescholar', [])
        }}
        )

