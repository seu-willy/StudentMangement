from django.shortcuts import render
from django.http import JsonResponse
from app01 import models
from django.views.decorators.csrf import csrf_exempt
import random
from datetime import datetime
from app01.utils.Pagination import Pagination
from app01.utils.MyForm import OrderModelForm



def order_list(request):
    '''订单列表'''
    queryset = models.Order.objects.all().order_by('-id')
    page_object = Pagination(request, queryset)
    form = OrderModelForm()
    context = {
        'form': form,
        'queryset': page_object.page_queryset,  # 分完页的数据
        'page_str': page_object.html()  # 页码
    }
    return render(request, "order_list.html", context)


@csrf_exempt
def order_add(request):
    '''添加订单（ajax方法）'''
    form = OrderModelForm(request.POST)
    if form.is_valid():
        form.instance.oid = datetime.now().strftime("%Y%m%d%H%M%S") + str(random.randint(1000, 9999))
        form.instance.user_id = request.session['info'].get('id')
        form.save()
        return JsonResponse({'status': True})
    return JsonResponse({'status': False, 'error': form.errors})

def order_delete(request):
    '''删除订单（ajax方法）'''
    uid = request.GET.get('uid')
    exists = models.Order.objects.filter(id=uid).exists()
    if not exists:
        return JsonResponse({'status': False, 'error':'删除失败，商品不存在！'})
    models.Order.objects.filter(id=uid).delete()
    return JsonResponse({'status': True})

def order_detail(request):
    '''获取编辑订单详情（ajax方法）'''
    uid = request.GET.get('uid')
    exists = models.Order.objects.filter(id=uid).exists()
    if not exists:
        return JsonResponse({'status': False, 'error':'编辑失败，商品不存在！'})
    row_dict = models.Order.objects.filter(id=uid).values('title','price','status').first()
    result = {
        'status': True,
        'data': row_dict
    }
    return JsonResponse(result)

@csrf_exempt
def order_edit(request):
    '''编辑订单（ajax方法）'''
    uid = request.GET.get('uid')
    row_object = models.Order.objects.filter(id=uid).first()
    if not row_object:
        return JsonResponse({'status': False, 'tip': '编辑失败，商品不存在！'})
    form = OrderModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return JsonResponse({'status': True})
    return JsonResponse({'status': False, 'error': form.errors})