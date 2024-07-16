from django.shortcuts import render, redirect
from app01 import models
from app01.utils.Pagination import Pagination
from app01.utils.MyForm import AdminModelModelForm, AdminResetModelModelForm, AdminEditModelModelForm

def admin_list(request):
    # 构造搜索条件
    filter_dict = {}
    search_data = request.GET.get('q', '')
    if search_data:
        filter_dict['username__contains'] = search_data

    # 根据搜索条件去数据库取数据
    queryset = models.Admin.objects.filter(**filter_dict)

    # 分页
    page_object = Pagination(request, queryset)

    context = {
        'queryset': page_object.page_queryset,
        'search_data': search_data,
        'page_str': page_object.html()
    }
    return render(request, "admin_list.html", context)

def admin_add(request):
    title = '新建管理员'
    if request.method == 'GET':
        form = AdminModelModelForm()
        return render(request, "change.html", {'form': form, 'title': title})
    form2 = AdminModelModelForm(request.POST)
    if form2.is_valid():
        form2.save()
        return redirect("/admin/list/")
    return render(request, "change.html", {'form': form2, 'title': title})

def admin_edit(request, nid):
    title = '修改管理员'
    row_object = models.Admin.objects.filter(id=nid).first()
    if not row_object:  # 判断存不存在，有可能多用户在线，你想编辑的时候，别人已经删了
        # return 错误页面
        return redirect("/admin/list/")
    if request.method == 'GET':
        form = AdminEditModelModelForm(instance=row_object)
        return render(request, "change.html", {'form':form,'title': title})
    form2 = AdminEditModelModelForm(data=request.POST, instance=row_object)
    if form2.is_valid():
        form2.save()
        return redirect("/admin/list/")
    return render(request, "change.html", {'form': form2, 'title': title})

def admin_delete(request, nid):
    models.Admin.objects.filter(id=nid).delete()
    return redirect("/admin/list/")

def admin_reset(request, nid):
    row_object = models.Admin.objects.filter(id=nid).first()
    if not row_object:
        return redirect("/admin/list/")

    title = f'重置密码——{row_object.username}'

    if request.method == 'GET':
        form = AdminResetModelModelForm()
        return render(request, "change.html", {'form':form,'title': title})
    form2 = AdminResetModelModelForm(data=request.POST, instance=row_object)
    if form2.is_valid():
        form2.save()
        return redirect("/admin/list/")
    return render(request, "change.html", {'form': form2, 'title': title})