import math
from django.shortcuts import render, redirect, HttpResponse
from app01 import models
from app01.utils.Pagination import Pagination
import pandas as pd
# 部门操作
def depart_list(request):
    '''部门列表'''
    # 去数据库获取部门列表
    filter_dict = {}
    search_data = request.GET.get('q', '')
    if search_data:
        filter_dict['title__contains'] = search_data
    queryset = models.Department.objects.filter(**filter_dict)
    page_object = Pagination(request, queryset, page_size=10)
    context = {
                'search_data': search_data,
                'queryset': page_object.page_queryset,
                'page_str': page_object.html()
               }
    return render(request, 'depart_list.html', context)
def depart_add(request):
    '''添加部门'''
    if request.method == "GET":
        return render(request, 'depart_add.html')
    # 获取用户通过post提交的数据
    title = request.POST.get('title')
    #  保存到数据库
    models.Department.objects.create(title=title)
    return redirect('/depart/list/')
def depart_delete(request):
    '''删除部门'''
    nid = request.GET.get('nid')

    models.Department.objects.filter(id=nid).delete()

    return redirect('/depart/list/')
def depart_edit(request, nid):
    '''编辑部门'''
    if request.method == "GET":
        data = models.Department.objects.filter(id=nid).first()
        return render(request, 'depart_edit.html', {'data': data})
    new_title = request.POST.get('title')
    models.Department.objects.filter(id=nid).update(title=new_title)
    return redirect('/depart/list/')

def dapart_multi(request):
    '''批量添加'''
    excel_object = request.FILES.get("exc")
    data_list = pd.read_excel(excel_object)['部门'].tolist()
    for i in data_list:
        exists = models.Department.objects.filter(title=i).exists()
        if not exists:
            models.Department.objects.create(title=i)
    return redirect('/depart/list/')