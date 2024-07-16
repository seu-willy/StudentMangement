from django.shortcuts import HttpResponse
from django_redis import get_redis_connection

def index(request):
    coon = get_redis_connection('default')
    coon.set('name', 'willy', ex=10)

    value = coon.get('name')
    print(value)
    return HttpResponse('ok')