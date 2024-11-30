from pathlib import Path
import logging
from user import User
import config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

USER_NAME = 'Lyon'
USER_ID = '0001'

class SelfScore:

    def __init__(self):
        self.user = User(id=USER_ID, name=USER_NAME)

    def run(self):
        self.welcome()
    
    def welcome(self):
        print("Welcome to SelfScore!")
        print('----------------------------')
        print(f"User: {self.user.name}")
        print(f'ID: {self.user.id}')
        self.user.show_user_data()
        print('----------------------------')

def main():
    selfscore = SelfScore()
    selfscore.run()

def test():
    user_obj = User(USER_ID, USER_NAME)
    user_obj.test()

if __name__ == "__main__":
    main()