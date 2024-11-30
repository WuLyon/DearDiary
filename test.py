from DearDiary import DearDiary
from user import User
from subject import Subject
import config


user = User(config.USER_ID, config.USER_NAME)
user.show_user_data()