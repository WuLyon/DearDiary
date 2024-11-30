class Subject:

    def __init__(self, name, point=0):
        self.name = name
        self.point = point
        
    def __repr__(self):
        '''
        格式化打印subject对象时的输出
        '''
        return f'Subject(name={self.name}, point={self.point})'
        
    def to_dict(self):
        '''
        subject对象转化为字典
        '''
        return {'subject': self.name, 'point': self.point}

    
    @classmethod
    def from_dict(cls, obj):
        '''
        将字典对象转化为subject对象
        '''
        return cls(obj['subject'], obj['point'])