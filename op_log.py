import datetime
import logging
from subject import Subject
import config


logger = logging.getLogger(__name__)

class OpLog():
    """
    记录每日得分情况的类
    """
    
    def __init__(self, day=datetime.date.today(), subjects=[]):

        self.day = day
        self.subjects = subjects
        if not self.subjects:
            self.default_subjects()
        

    def __repr__(self):

        return f'OpLog(day={self.day}, subjects={self.subjects})'
        

    def add_subject(self, name):

        self.subjects.append(Subject(name))
        

    def default_subjects(self):

        for subject in config.DEFAULT_SUBJECT:
            self.add_subject(subject)
        
        
    def to_dict(self):
        
        subject_list = [subject.to_dict() for subject in self.subjects]
        return {'day': self.day.strftime('%Y-%m-%d'), 'subjects': subject_list}
    
    
    @classmethod
    def from_dict(cls, obj):

        day = datetime.datetime.strptime(obj['day'], '%Y-%m-%d').date()
        subjects = [Subject.from_dict(subject) for subject in obj['subjects']]

        return cls(day, subjects)