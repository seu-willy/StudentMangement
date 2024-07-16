import math
from django.shortcuts import render, redirect
from app01 import models
from app01.utils.Pagination import Pagination
from app01.utils.MyForm import PreetyNumModelForm,PreetyEditModelForm




# 靓号操作
def num_list(request):
    '''靓号列表'''
    # 数值型
    # q1 = models.PreetyNum.objects.filter(id=2)  # id=
    # q2 = models.PreetyNum.objects.filter(id__gt=3)  # id>
    # q3 = models.PreetyNum.objects.filter(id__gte=5)  # id>=
    # q4 = models.PreetyNum.objects.filter(id__lt=5)  # id<
    # q5 = models.PreetyNum.objects.filter(id__lte=3)  # id<=

    # 文本型
    # q1 = models.PreetyNum.objects.filter(mobile__startswith='177')  # 以177开头  ^177\d+
    # q2 = models.PreetyNum.objects.filter(mobile__endswith='8213')  # 以8213结尾   \d+8213$
    # q3 = models.PreetyNum.objects.filter(mobile__contains='888')  # 以包含888  \d+888\d*

    # 以字典形式
    # filter_dict = {'mobile__contains':'888'}
    # q1 = models.PreetyNum.objects.filter(**filter_dict)
    # print(q1)
    # for i in range(300):
    #     models.PreetyNum.objects.create(mobile=str(random.randint(13162851020, 18815683215)), price=random.randint(100,1000), level=random.randint(1,4), status=random.randint(1,2))
    # import copy
    # query_dict = copy.deepcopy(request.GET)
    # query_dict._mutable = True
    # query_dict.setlist('num',[111])
    # print(query_dict.urlencode())
    filter_dict = {}
    search_data = request.GET.get('q', '')
    if search_data:
        filter_dict['mobile__contains'] = search_data
    queryset = models.PreetyNum.objects.filter(**filter_dict)
    page_object = Pagination(request, queryset)
    context = {
        'search_data': search_data,
        'queryset': page_object.page_queryset,  # 分完页的数据
        'page_str': page_object.html()  # 页码
    }
    return render(request, "num_list.html", context)

def num_add(request):
    if request.method == "GET":
        form = PreetyNumModelForm()
        return render(request, "num_add.html", {'form': form})
    form2 = PreetyNumModelForm(request.POST)

    if form2.is_valid():
        form2.save()
        return redirect('/num/list/')
    return render(request, "num_add.html", {'form': form2})
def num_edit(request, nid):
    row_data = models.PreetyNum.objects.filter(id=nid).first()
    if request.method == 'GET':
        form = PreetyEditModelForm(instance=row_data)
        return render(request, "num_edit.html", {'form': form})
    form2 = PreetyEditModelForm(request.POST, instance=row_data)
    if form2.is_valid():
        form2.save()
        page = math.ceil(nid/10)
        return redirect(f'/num/list/?page={page}')
    return render(request, "num_edit.html", {'form': form2})
def num_delete(request, nid):
    models.PreetyNum.objects.filter(id=nid).delete()
    return redirect('/num/list/')