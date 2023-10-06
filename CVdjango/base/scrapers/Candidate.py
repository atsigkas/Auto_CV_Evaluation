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
                "publications": self.candidate['publications'],
                "researchgate": self.candidate.get('researchgate', []),
                "googlescholar": self.candidate.get('googlescholar', [])
        }}
        )
    def update_candidate_after_url(self, col):
        col.update_one(
            {"_id": self.candidate['_id']},
            {"$set": {
                "researchgate_url":self.candidate["researchgate_url"],
                "googlescholar_url":self.candidate["googlescholar_url"],
                "publications": self.candidate['publications'],
                "researchgate": self.candidate.get('researchgate', []),
                "googlescholar": self.candidate.get('googlescholar', [])
        }}
        )

    def to_dict(self):
        return self.__dict__
