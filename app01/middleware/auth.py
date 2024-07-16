from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect


class AuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.path_info in ['/login/', '/image/code/'] :
            return  # 默认返回none 向下走
        data_dict = request.session.get('info')
        # print(data_dict)
        if data_dict:
            return  # 默认返回none 向下走
        return redirect('/login/')  # 重定向，回去，不会往后走到视图函数
