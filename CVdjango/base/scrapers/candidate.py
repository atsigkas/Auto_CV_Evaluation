class Candidate:
    def __init__(self, data=None):
        self.candidate = {}
        if data:
            self.override_data(data)

    def override_data(self, new_data):
        self.candidate.update(new_data)

    def insert_candidate(self, col):
        col.insert_one(self.candidate)