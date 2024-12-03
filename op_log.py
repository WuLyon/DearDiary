import datetime
import logging
from subject import Subject
import config


logger = logging.getLogger(__name__)

class OpLog():
    """
    记录每日得分情况的类
    """
    
    def __init__(self, day=datetime.date.today(), subjects=None):

        self.day = day
        self.subjects = subjects if subjects is not None else []
        if not self.subjects:
            self.default_subjects()
            
        self.day_point = self.calculate_day_point()
        
    
    def calculate_day_point(self):
        day_point = 0
        for subject in self.subjects:
            day_point += subject.point
        self.day_point  = day_point
        return day_point
        

    def __repr__(self):

        return f'OpLog(day={self.day}, day_point={self.day_point}, subjects={self.subjects})'
        

    def add_subject(self, name):

        self.subjects.append(Subject(name))
        

    def default_subjects(self):

        for subject in config.DEFAULT_SUBJECT:
            self.add_subject(subject)
        
        
    def to_dict(self):
        
        day = self.day.strftime('%Y-%m-%d')
        subject_list = [subject.to_dict() for subject in self.subjects]
        day_point = self.calculate_day_point()
        return {'day': day, 'day_point': day_point, 'subjects': subject_list}
    
    
    @classmethod
    def from_dict(cls, obj):

        day = datetime.datetime.strptime(obj['day'], '%Y-%m-%d').date()
        subjects = [Subject.from_dict(subject) for subject in obj['subjects']]

        return cls(day, subjects)