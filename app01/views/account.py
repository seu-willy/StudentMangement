from django.shortcuts import render, HttpResponse, redirect
from django import forms
from app01.utils.BootstrpForm import BootstrpForm
from app01.utils.encrypt import md5
from app01 import models
from app01.utils.code import check_code
from io import BytesIO
from app01.utils.MyForm import LoginForm


def login(request):
    '''登录'''
    if request.method == 'GET':
        form = LoginForm()
        return render(request, "login.html", {'form': form})
    form2 = LoginForm(data=request.POST)
    if form2.is_valid():
        code_input = form2.cleaned_data.pop('code')
        code_image = request.session.get('image')
        if code_input.upper() != code_image.upper():
            form2.add_error("code", "验证码错误！")
            return render(request, "login.html", {'form': form2})

        row_object = models.Admin.objects.filter(**form2.cleaned_data).first()  # 本身返回的是一个字典，字典可以作为筛选参数传入
        if not row_object:
            form2.add_error("password", "用户名或密码错误")  # form对象可以添加错误，在密码下面出现
            return render(request, "login.html", {'form': form2})
        # 将用户登录的信息生成Cookie,写入Session
        request.session['info'] = {'id': row_object.id, 'name': row_object.username}
        request.session.set_expiry(60 * 60 * 24 * 7)  # 重新将session的有效期拉长，避免操作了60s就过期了
        return redirect('/admin/list/')
    return render(request, "login.html", {'form': form2})


def image_code(request):
    '''生成图片验证码'''
    img, code_string = check_code()  # 调用函数生成验证码和图片
    request.session['image'] = code_string  # 将验证码写入session，方便在登录的地方验证，有点像实例属性，大家都能用
    request.session.set_expiry(60)  # 给session设置时长，这里是为了避免验证图片一直有效
    stream = BytesIO()
    img.save(stream, 'png')

    return HttpResponse(stream.getvalue())

def logout(request):
    '''注销用户'''
    request.session.clear()
    return redirect('/login/')
