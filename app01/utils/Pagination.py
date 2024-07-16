'''
分页类,使用说明：
##1导入类 from app01.utils.Pagination import Pagination
##2实例化分页对象 page_object = Pagination(request, queryset,……)
##3定义传入前端的字典
    context = {
            'queryset': page_object.page_queryset,  # 分完页的数据
            'page_str': page_object.html()  # 页码
        }
    return render(request, "user_list.html", context)
##4前端需要加入页码
    循环数据
    {% for obj in queryset %}
        <tr>
            <td>{{ obj.xxxxx }}</td>
        </tr>
    {% endfor %}
    配置页码
    <ul class="pagination">
        {{ page_str | safe }}
    </ul>

'''
import math
import copy
class Pagination(object):
    def __init__(self, request, queryset, page_size=10, page_width=5, page_param='page'):
        '''

        :param request: 传递的request请求
        :param queryset:  筛选好的数据
        :param page_size:  每页展示的数据数
        :param page_width:  当前页码 前或后n页
        :param page_param:   url传递的参数，例如/num/list/?page=2
        '''

        query_dict = copy.deepcopy(request.GET)  # 深拷贝request.GET,可以修改源码，实现在原来的url参数的基础上增加页码参数的功能
        query_dict._mutable = True  # 修改_mutable属性为True，可以为query_dict对象传入参数
        self.query_dict = query_dict

        page = request.GET.get(page_param, '1')
        if page.isdecimal():
            page = int(page)
        else:
            page = 1
        self.page = page
        self.page_size = page_size
        self.page_width = page_width
        self.page_param = page_param
        self.start = (page - 1) * page_size
        self.end = page * page_size
        self.page_queryset = queryset[self.start:self.end]
        total_num = queryset.count()
        total_page = math.ceil(total_num / page_size)
        self.total_page = total_page
    def html(self):
        page_list = []
        self.query_dict.setlist(self.page_param, [1])
        first = f'<li><a href="?{self.query_dict.urlencode()}" aria-label="Previous"><span aria-hidden="true">首页</span></a></li>'
        page_list.append(first)
        self.query_dict.setlist(self.page_param, [self.page - 1])
        pre = f'<li><a href="?{self.query_dict.urlencode()}" aria-label="Previous"><span aria-hidden="true">«</span></a></li>'
        if self.page == 1:
            self.query_dict.setlist(self.page_param, [1])
            pre = f'<li><a href="?{self.query_dict.urlencode()}" aria-label="Previous"><span aria-hidden="true">«</span></a></li>'
        page_list.append(pre)
        if self.total_page <= 2*self.page_width+1:
            for i in range(1, self.total_page+1):
                self.query_dict.setlist(self.page_param, [i])
                tql = f'<li><a href="?{self.query_dict.urlencode()}">{i}</a></li>'
                if i == self.page:
                    tql = f'<li class="active"><a href="?{self.query_dict.urlencode()}">{i}<span class="sr-only">(current)</span></a></li>'
                page_list.append(tql)
        else:
            if self.page > self.page_width and self.page < self.total_page - self.page_width + 1:
                for i in range(self.page - self.page_width, self.page + self.page_width +1):
                    self.query_dict.setlist(self.page_param, [i])
                    tql = f'<li><a href="?{self.query_dict.urlencode()}">{i}</a></li>'
                    if i == self.page:
                        tql = f'<li class="active"><a href="?{self.query_dict.urlencode()}">{i}<span class="sr-only">(current)</span></a></li>'
                    page_list.append(tql)
            elif self.page <= self.page_width:
                for i in range(1, (self.page_width + 1) * 2):
                    self.query_dict.setlist(self.page_param, [i])
                    tql = f'<li><a href="?{self.query_dict.urlencode()}">{i}</a></li>'
                    if i == self.page:
                        tql = f'<li class="active"><a href="?{self.query_dict.urlencode()}">{i}<span class="sr-only">(current)</span></a></li>'
                    page_list.append(tql)
            else:
                for i in range(self.total_page - self.page_width * 2, self.total_page + 1):
                    self.query_dict.setlist(self.page_param, [i])
                    tql = f'<li><a href="?{self.query_dict.urlencode()}">{i}</a></li>'
                    if i == self.page:
                        tql = f'<li class="active"><a href="?{self.query_dict.urlencode()}">{i}<span class="sr-only">(current)</span></a></li>'
                    page_list.append(tql)
        self.query_dict.setlist(self.page_param, [self.page + 1])
        next = f'<li><a href="?{self.query_dict.urlencode()}" aria-label="Next"><span aria-hidden="true">»</span></a></li>'
        if self.page == self.total_page:
            self.query_dict.setlist(self.page_param, [self.total_page])
            next = f'<li><a href="?{self.query_dict.urlencode()}" aria-label="Next"><span aria-hidden="true">»</span></a></li>'
        page_list.append(next)
        self.query_dict.setlist(self.page_param, [self.total_page])
        last = f'<li><a href="?{self.query_dict.urlencode()}" aria-label="Previous"><span aria-hidden="true">尾页</span></a></li>'
        page_list.append(last)
        jump_str = '''
            <li>
                <form class="navbar-form navbar-left" method="get" style="margin:0">
                    <input type="text" name="page" class="form-control" placeholder="页码" style="width: 60px">
                    <button type="submit" class="btn btn-default">跳转到</button>
                </form>
            </li>
            '''
        page_list.append(jump_str)
        page_str = ''.join(page_list)
        return page_str