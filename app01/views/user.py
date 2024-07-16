from django.shortcuts import render, redirect
from app01 import models
from app01.utils.Pagination import Pagination
from app01.utils.MyForm import UserModelForm

# 用户操作
def user_list(request):
    filter_dict = {}
    search_data = request.GET.get('q', '')
    if search_data:
        filter_dict['name__contains'] = search_data
    queryset = models.UserInfo.objects.filter(**filter_dict)
    page_object = Pagination(request, queryset)
    context = {
        'search_data': search_data,
        'queryset': page_object.page_queryset,  # 分完页的数据
        'page_str': page_object.html()  # 页码
    }
    return render(request, "user_list.html", context)
    # for obj in queryset:
    #     print(obj.name, obj.password, obj.age, obj.account, obj.create_time.strftime('%Y-%m-%d'))  # 时间格式化为字符串
    #     print(obj.gender, obj.get_gender_display())  # django内置的获取choice元组内容的方法
    #     print(obj.depart_id, obj.depart.title)  # django内置的获取关联表内容的方法
def user_add(request):
    if request.method == "GET":
        return render(request, "user_add.html", {"depart_list": models.Department.objects.all()})
    data = request.POST
    name = data.get('name')
    age = data.get('age')
    password = data.get('password')
    create_time = data.get('create_time')
    gender = data.get('gender')
    depart = data.get('depart')
    print(name, password, create_time, gender, depart)
    models.UserInfo.objects.create(name=name, age=age, password=password, create_time=create_time, gender=gender,
                                   depart_id=depart)
    return redirect('/user/list/')
def user_model_form_add(request):
    if request.method == "GET":
        form = UserModelForm()  # 定义一个modelform对象，表是 UserInfo,含有的字段是 fields = ['name', 'age', 'password', 'create_time', 'gender', 'depart']
        # print(form)    # 内容是基于字段生成的html标签[obj1, obj2…………] 每个obj是一个div字段，里面有label和input标签
        # print(type(form))  # <class 'app01.views.UserForm'>
        return render(request, "user_model_form_add.html", {'form': form})
    form2 = UserModelForm(request.POST)  # 定义一个modelform对象，它是由传回的那个[obj1,obj2…………],包含了label、input、error等信息
    print(request.POST)
    print(type(request.POST))  # <class 'django.http.request.QueryDict'>
    # print(form2)  # 内容是基于用户上传生成的html标签[obj1, obj2…………]，里面包含用户选择的信息
    # print(type(form2))  # <class 'app01.views.UserForm'>
    if form2.is_valid():
        # form2.instance.account = 1283
        form2.save()
        return redirect('/user/list/')
    return render(request, "user_model_form_add.html", {'form': form2})
def user_edit(request, nid):
    row_data = models.UserInfo.objects.filter(id=nid).first()
    if request.method == 'GET':
        form = UserModelForm(instance=row_data)
        return render(request, "user_edit.html", {'form': form})
    form2 = UserModelForm(request.POST, instance=row_data)
    if form2.is_valid():
        # form2.instance.account = 546.98
        form2.save()
        return redirect('/user/list/')
    return render(request, "user_edit.html", {'form': form2})

def user_delete(request, nid):
    models.UserInfo.objects.filter(id=nid).delete()
    return redirect('/user/list/')