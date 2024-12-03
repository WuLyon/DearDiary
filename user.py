from subject import Subject
from op_log import OpLog
import datetime
import json
import logging
import config

logger = logging.getLogger(__name__)

class User:

    def __init__(self, id=config.USER_ID, name=config.USER_NAME):
        self.id = id
        self.name = name
        self.score = 0
        self.op_logs = []
        self.data_path = self.get_data_path()   # 获取用户数据储存的路径
        self.load_data()    # 加载用户数据
        self.count = 0  # 临时记录一个函数被调用了多少次


    def add_op(self, day=datetime.date.today()):
        '''
        添加操作记录
        '''
        last_op = self.op_logs[-1]

        if day == last_op.day:
            for i in range(len(last_op.subjects)):
                is_done = input(f'Have you did {last_op.subjects[i].name}? (y/n)')
                if is_done.lower() == 'y':
                    if len(self.op_logs) > 1:   # 避免访问不到self.op_logs[-2]
                        last_op.subjects[i].point = self.op_logs[-2].subjects[i].point + 1
                    else:   # 当不存在self.op_logs[-2]时，直接+1
                        last_op.subjects[i].point += 1
            self.op_logs[-1].calculate_day_point()
            self.update_data()
        else:
            new_log = OpLog(day=last_op.day + datetime.timedelta(days=1))
            self.op_logs.append(new_log)
            self.add_op()
            
    def calculate_score(self):
        '''
        计算总分
        '''
        self.score = 0
        for op_log in self.op_logs:
            self.score += op_log.day_point



    def new_data(self):
        '''
        初始化一个新用户的初始数据
        '''

        # 初始化数据
        self.op_logs.append(OpLog())
        data = {
            'user_id': self.id,
            'user_name': self.name,
            'op_logs': self.op_logs,
            'score': self.score
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
        # 判断是否是新用户，新用户则创建新的json数据文件，否则直接获取json文件的路径
        if not data_path.exists():
            data = self.new_data() # 初始化数据
            with data_path.open('w') as f:
                json.dump(data, f, default=oplog_to_dict, indent=4)    # 将subject对象转化为字典后存入json文件
            logger.info(f'Created new data path {data_path}')
        else:
            logger.info(f'Found data path: {data_path}')
        return data_path
    
    def update_data(self):
        '''
        更新用户数据
        '''
        self.calculate_score()
        data = {
            'user_id': self.id,
            'user_name': self.name,
            'op_logs': self.op_logs,
            'score': self.score
        }
        # 同步新数据到json文件
        logger.info(f'Saving data of user {self.name} {self.id}')
        try:
            with self.data_path.open('w') as f:
                json.dump(data, f, default=oplog_to_dict, indent=4)  # 将subject对象转化为字典后存入json文件
        except Exception as e:
            logger.error(f'An unexpected error occurred while writing {self.data_path}: {e}')



    def load_data(self):
        '''
        从json文件加载用户数据
        '''
        try:
            with self.data_path.open('r') as f:
                data = json.load(f, object_hook=dict_to_oplog)    # 将json文件中的subject字典转化为subject对象
            self.name = data['user_name']
            self.op_logs = data['op_logs']
            self.score = data['score']
            logger.info(f'Get user data successfully!')
            return data
        except Exception as e:
            logger.error(f'An unexpected error occurred while writing {self.data_path}: {e}')
        return None 
    
            
    def __repr__(self):
        '''
        打印用户数据到终端
        '''
        total_days = len(self.op_logs)
        return f'user_id: {self.id}\nuser_name: {self.name}\nop_logs: {self.op_logs}\nscore: {self.score}\ntotal_days: {total_days}\n'
        


def oplog_to_dict(obj):
    '''
    将OpLog对象转化为字典
    '''
    if isinstance(obj, OpLog):
        return obj.to_dict()
    
def dict_to_oplog(obj):
    '''
    将字典对象转化为oplog对象
    '''
    if 'day' in obj and 'day_point' in obj and 'subjects' in obj:
        return OpLog.from_dict(obj)
    return obj