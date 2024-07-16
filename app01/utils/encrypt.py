import hashlib
from django.conf import settings

def md5(data_string):
    obj = hashlib.md5(settings.SECRET_KEY.encode('utf-8'))  # 导入django自带的盐，随机密码SECRET_KEY = 'django-insecure-_py4tzzp)$!@j1@r0j05)-@g0*4$4os6+s44m8+q+8*uvjl)g$'
    obj.update(data_string.encode('utf-8'))
    return obj.hexdigest()