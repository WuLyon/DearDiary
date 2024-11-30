from subject import Subject
import datetime
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
        self.days = []
        self.data_path = self.get_data_path()   # 获取用户数据储存的路径
        self.load_data()    # 加载用户数据

    def operator(self):
        today = datetime.date.today()
        for subject in self.subjects:
            is_done = input(f'{subject.name}: ')
            if is_done.lower() == 'y':
                subject.point += 1
                

    def add_subject(self, name):
        '''
        向subjects列表中添加新的subject对象
        name: subject的名称
        '''
        self.subjects.append(Subject(name))
        

    def new_data(self):
        '''
        初始化一个新用户的初始数据
        '''
        # 向subjects列表中添加预设的subject
        for subject in config.DEFAULT_SUBJECT:
            self.add_subject(subject)

        # 初始化数据
        data = {
            'user_id': self.id,
            'user_name': self.name,
            'subjects': self.subjects,
            'score': 0
        }
        logger.info(f'Setup a new user data: {data}')
        return data
        
    def change_user_name(self, new_name):
        self.name = new_name
        self.update_data()
        logger.info(f'Have changed the user name into {self.name}')

    def get_data_path(self):
        '''
        获取用户数据的储存路径，若路径存在，直接返回；若路径不存在，则新建json文件并初始化数据
        '''
        data_path = config.APP_PATH / 'users' / (self.id + ".json")
        if not data_path.exists():
            data = self.new_data() # 初始化数据
            with data_path.open('w') as f:
                json.dump(data, f, default=subject_to_dict, indent=4)    # 将subject对象转化为字典后存入json文件
            logger.info(f'Created new data path {data_path}')
        else:
            logger.info(f'Found data path: {data_path}')
        return data_path
    
    def update_data(self):
        '''
        更新用户数据
        '''
        data = {
            'user_id': self.id,
            'user_name': self.name,
            'subjects': self.subjects,
            'score': self.score
        }
        # 同步新数据到json文件
        logger.info(f'Saving data of user {self.name} {self.id}')
        try:
            with self.data_path.open('w') as f:
                json.dump(data, f, default=subject_to_dict, indent=4)  # 将subject对象转化为字典后存入json文件
        except Exception as e:
            logger.error(f'An unexpected error occurred while writing {self.data_path}: {e}')



    def load_data(self):
        '''
        从json文件加载用户数据
        '''
        try:
            with self.data_path.open('r') as f:
                data = json.load(f, object_hook=dict_to_subject)    # 将json文件中的subject字典转化为subject对象
            self.name = data['user_name']
            self.subjects = data['subjects']
            self.score = data['score']
            logger.info(f'Get user data successfully!')
            return data
        except Exception as e:
            logger.error(f'An unexpected error occurred while writing {self.data_path}: {e}')
        return None 
    
            
    def show_user_data(self):
        '''
        打印用户数据到终端
        '''
        print(
           f'user_id: {self.id}\n' + 
           f'user_name: {self.name}\n' + 
           f'subjects: {self.subjects}\n' +
           f'score: {self.score}'
        )
        


def subject_to_dict(obj):
    '''
    将subject对象转化为字典
    '''
    if isinstance(obj, Subject):
        return obj.to_dict()
    
def dict_to_subject(obj):
    '''
    将字典对象转化为subject对象
    '''
    if 'subject' in obj and 'point' in obj:
        return Subject.from_dict(obj)
    return obj