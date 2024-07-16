import os
from django.shortcuts import render, HttpResponse
from django import forms
from app01.utils.BootstrpForm import BootstrpForm, BootstrapModelForm
from app01 import models
from django.conf import settings


def file_upload(request):
    if request.method == 'GET':
        return render(request, "file_upload.html")
    data = request.POST
    file_object = request.FILES.get('file')
    # print(data)
    # print(file)
    with open(file_object.name, mode='wb') as f:
        for chunk in file_object.chunks():
            f.write(chunk)
    return HttpResponse("File Uploaded")


class UpForm(BootstrpForm):
    bootstrap_exclude_fields = ['img']
    name = forms.CharField(label='姓名')
    age = forms.CharField(label='年龄')
    img = forms.FileField(label='头像')


def upload_form(request):
    title = "Form 上传"
    if request.method == 'GET':
        form = UpForm()
        return render(request, "upload_form.html", {'form': form, 'title': title})
    form2 = UpForm(data=request.POST, files=request.FILES)  # 有文件格式需要写files=request.Files
    if form2.is_valid():
        # 通过form的形式，需要自己单独处理得到的字段
        # 图像需要先保存在路径，再把路径传给数据库
        img_obj = form2.cleaned_data.get('img')
        media_path = os.path.join('media', img_obj.name)
        f = open(media_path, mode='wb')
        for chunk in img_obj.chunks():
            f.write(chunk)
        f.close()
        name = form2.cleaned_data.get('name')
        age = form2.cleaned_data.get('age')
        img = media_path
        models.Boss.objects.create(name=name, age=age, img=img, )

        return HttpResponse('上传成功')
    return render(request, "upload_form.html", {'form': form2, 'title': title})


class CityModelForm(BootstrapModelForm):
    bootstrap_exclude_fields = ['img']
    class Meta:
        model = models.City
        fields = "__all__"


def upload_modelform(request):
    title = "ModelForm上传"
    if request.method == 'GET':
        form = CityModelForm()
        return render(request, "upload_form.html", {'form': form, 'title': title})
    form2 = CityModelForm(data=request.POST, files=request.FILES)
    if form2.is_valid():
        form2.save()  # modelform可以直接帮你搞定文件写入media/city/文件夹，文件路径写入数据库
        return HttpResponse('上传成功！')
    return render(request, "upload_form.html", {'form': form2, 'title': title})