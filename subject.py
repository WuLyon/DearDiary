class Subject:

    def __init__(self, name, score=0):
        self.name = name
        self.score = score
        
    def get_subject_dict(self):
        return {'subject': self.name, 'score': self.score}