from django.shortcuts import render, redirect
from app01 import models
from app01.utils.BootstrpForm import BootstrapModelForm

def city_list(request):
    queryset = models.City.objects.all()
    return render(request, "city_list.html", {'queryset':queryset})

class CityModelForm(BootstrapModelForm):
    bootstrap_exclude_fields = ['img']
    class Meta:
        model = models.City
        fields = "__all__"

def city_add(request):
    title = "新建城市"
    if request.method == 'GET':
        form = CityModelForm()
        return render(request, "upload_form.html", {'form': form, 'title': title})
    form2 = CityModelForm(data=request.POST, files=request.FILES)
    if form2.is_valid():
        form2.save()  # modelform可以直接帮你搞定文件写入media/city/文件夹，文件路径写入数据库
        return redirect("/city/list/")
    return render(request, "upload_form.html", {'form': form2, 'title': title})