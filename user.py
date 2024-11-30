from pathlib import Path
from subject import Subject
import json
import logging
import config

logger = logging.getLogger(__name__)

class User:

    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.subjects = []
        self.score = 0
        self.data_path = self.get_data_path()
        self.data = self.load_data()
        
    def add_subject(self, name):
        subject = Subject(name)
        self.subjects.append(subject.get_subject_dict())
        self.update_data()
        
    def add_default_subject(self):
        subject_list = [
            'Python',
            'Math',
            'English',
            'Exercise',
            'Reading',
            'Paint',
            'Hygiene',
            'Cardistry',
            'Film',
            'Music',
            'Meditation',
            'Nosex',
            'Sleep'
        ]
        for subject in subject_list:
            self.add_subject(subject)
    
    def new_data(self):
        self.add_default_subject()
        data = {
            'user_id': self.id,
            'user_name': self.name,
            'subjects': self.subjects,
            'score': 0
        }
        logger.info(f'Setup a new user data: {data}')
        return data
        
    def get_data_path(self):
        data_path = config.APP_PATH / 'users' / (self.id + ".json")
        if not data_path.exists():
            with data_path.open('w') as f:
                json.dump(self.new_data(), f, indent=4)
            logger.info(f'Created new data path {data_path}')
        else:
            logger.info(f'Found data path: {data_path}')
        return data_path
    
    def update_data(self):
        self.data = {
            'user_id': self.id,
            'user_name': self.name,
            'subjects': self.subjects,
            'score': self.score
        }
        self.data_path = self.get_data_path()
        self.save_user_data()


    def load_data(self):
        try:
            with self.data_path.open('r') as f:
                data = json.load(f)
            logger.info(f'Get user data successfully!')
            return data
        except Exception as e:
            logger.error(f'An unexpected error occurred while writing {self.data_path}: {e}')
        return None 
    
    def save_user_data(self):
        logger.info(f'Saving data of user {self.name} {self.id}')
        try:
            with self.data_path.open('w') as f:
                json.dump(self.data, f, indent=4)
        except Exception as e:
            logger.error(f'An unexpected error occurred while writing {self.data_path}: {e}')
            
    def show_user_data(self):
        print(self.data)
        logger.info(f'{self.name} {self.id} data is printed!')
        
    def show_subject_list(self):
        for subject in self.data['subjects']:
            print(subject['subject'])

    def test(self):
        self.show_user_data()
        self.show_subject_list()