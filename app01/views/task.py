import json
from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from app01 import models
from app01.utils.Pagination import Pagination
from app01.utils.MyForm import TaskModelForm


def task_list(request):
    queryset = models.TaskInfo.objects.all().order_by('-id')
    page_object = Pagination(request, queryset, page_size=5)
    form = TaskModelForm()
    context = {
        'form': form,
        'queryset': page_object.page_queryset,  # 分完页的数据
        'page_str': page_object.html()  # 页码
    }
    return render(request, "task_list.html", context)


@csrf_exempt
def task_ajax(request):
    print(request.POST)  # 接收ajax上传的数据
    print(request.POST.get('name'))  # 接收ajax上传的数据
    print(request.POST.get('age'))  # 接收ajax上传的数据
    data_dict = {
        "status": True,
        "data": [1, 2, 3, 4, 5, 6]
    }
    json_data = json.dumps(data_dict)
    return HttpResponse(json_data)  # 返回给ajax中success后函数的内容


@csrf_exempt
def task_add(request):
    print(request.POST)
    form = TaskModelForm(request.POST)
    if form.is_valid():
        form.save()
        data_dict = {"status": True}
        return HttpResponse(json.dumps(data_dict))

    data_dict = {"status": False, "error": form.errors}
    return HttpResponse(json.dumps(data_dict, ensure_ascii=False))
