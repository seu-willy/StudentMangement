from django.shortcuts import render
from django.http import JsonResponse


def chart_list(request):
    '''数据统计'''
    return render(request, "chart_list.html")


def chart_bar(request):
    series_list = [
        {
            'name': '销量',
            'type': 'bar',
            'data': [5, 20, 36, 10, 10, 20]
        },
        {
            'name': '业绩',
            'type': 'bar',
            'data': [15, 10, 26, 30, 15, 50]
        },
    ]
    x_axis = ['1月', '2月', '3月', '4月', '5月', '6月']
    legend = ['销量', '业绩']
    result = {
        'status': True,
        'data': {
            'series_list': series_list,
            'x_axis': x_axis,
            'legend': legend
        }
    }
    return JsonResponse(result)
