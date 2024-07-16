import re
from app01 import models
from django.core.validators import ValidationError
from app01.utils.BootstrpForm import BootstrapModelForm, BootstrpForm
from django import forms
from app01.utils.encrypt import md5

# '''user相关modelform'''
class UserModelForm(BootstrapModelForm):
    class Meta:
        model = models.UserInfo
        fields = "__all__"  # 使用所有字段

# '''num相关modelform'''
class PreetyNumModelForm(BootstrapModelForm):
    # 方式一：通过正则表达式对字段进行验证
    # mobile = forms.CharField(
    #     label = '靓号号码',
    #     validators = [RegexValidator(r'^1[3-9]\d{9}$', '手机号码格式错误')]

    class Meta:
        model = models.PreetyNum
        fields = ['mobile', 'price', 'level', 'status']
    # 方式二：通过钩子函数对字段进行验证
    def clean_mobile(self):
        data = self.cleaned_data['mobile']  # 拿到用户输入的文本
        exist = models.PreetyNum.objects.filter(mobile=data).exists()
        if exist:
            raise ValidationError("手机号码已存在")
        result = re.match(r'^1[3-9]\d{9}$', data)
        if not result:
            raise ValidationError("手机号格式错误！！")
        return data
class PreetyEditModelForm(BootstrapModelForm):
    # mobile = forms.CharField(disabled=True, label='靓号号码')  # 通过forms添加对象，不可修改
    class Meta:
        model = models.PreetyNum
        fields = ['mobile', 'price', 'level', 'status']
    def clean_mobile(self):
        id = self.instance.pk  # 你现在实例化的那一行（需要编辑的）的对象的pirmary key
        data = self.cleaned_data['mobile']  # 拿到用户输入的文本
        exist = models.PreetyNum.objects.exclude(id=id).filter(mobile=data).exists()  # 之所以要exclude，是因为，如果手机号码自己没有修改，只修改了其他属性，上传就会重复
        if exist:
            raise ValidationError("手机号码已存在")
        result = re.match(r'^1[3-9]\d{9}$', data)
        if not result:
            raise ValidationError("手机号格式错误！！")
        return data

# '''admin相关modelform'''
class AdminModelModelForm(BootstrapModelForm):
    # 创建新字段
    confirm_password = forms.CharField(
        label='确认密码',
        widget=forms.PasswordInput(render_value=True),
    )

    class Meta:
        model = models.Admin
        fields = ['username', 'password', 'confirm_password']
        widgets = {
            'password': forms.PasswordInput(render_value=True)
        }  # 更改原字段属性

    def clean_username(self):
        user_input = self.cleaned_data.get('username')
        exists = models.Admin.objects.filter(username=user_input).exists()
        if exists:
            raise ValidationError('管理员已存在！')
        match = re.match(r'^^[A-Z][a-z]*$', user_input)
        if not match:
            raise ValidationError('姓名格式有误！')
        return user_input
    def clean_password(self):
        pwd = self.cleaned_data['password']
        return md5(pwd)

    def clean_confirm_password(self):  # 需要验证a就 clean_a
        #  如果数据有效，form2.cleaned_data 返回用户传入的数据
        pwd = self.cleaned_data['password']
        confirm = md5(self.cleaned_data['confirm_password'])  # 由于password字段在前，先处理，所以会先加密，这里确认密码也需要加密，在比
        if pwd != confirm:
            raise ValidationError('密码不一致')
        return confirm  # 这里一定要返回clean_a中a字段，因为这个值会被save进数据库,这里confirm对应的confirm_password没有被保存
class AdminEditModelModelForm(BootstrapModelForm):
    class Meta:
        model = models.Admin
        fields = ['username']
    def clean_username(self):
        user_input = self.cleaned_data.get('username')
        exists = models.Admin.objects.filter(username=user_input).exists()
        if exists:
            raise ValidationError('管理员已存在！')
        match = re.match(r'^^[A-Z][a-z]*$', user_input)
        if not match:
            raise ValidationError('姓名格式有误！')
        return user_input
class AdminResetModelModelForm(BootstrapModelForm):
    confirm_password = forms.CharField(
        label='确认密码',
        widget=forms.PasswordInput(render_value=True),
    )
    class Meta:
        model = models.Admin
        fields = ['password', 'confirm_password']
        widgets = {
            'password': forms.PasswordInput(render_value=True)
        }  # 更改原字段属性

    def clean_password(self):
        pwd = self.cleaned_data.get('password')
        md5_pwd = md5(pwd)
        # print(md5_pwd)
        # print('self.instance', self.instance, self.instance.password, type(self.instance))  # self.instance Amanda 604444a7262ce663a50d1dfcf5af2c46 <class 'app01.models.Admin'>
        exists = models.Admin.objects.filter(id=self.instance.pk, password=md5_pwd).exists()
        if exists:
            raise ValidationError("密码不能与之前的一致")

        return md5_pwd

    def clean_confirm_password(self):  # 需要验证a就 clean_a
        #  如果数据有效，form2.cleaned_data 返回用户传入的数据
        pwd = self.cleaned_data.get('password')
        confirm = md5(self.cleaned_data.get('confirm_password'))  # 由于password字段在前，先处理，所以会先加密，这里确认密码也需要加密，在比
        if pwd != confirm:
            raise ValidationError('密码不一致')
        return confirm  # 这里一定要返回clean_a中a字段，因为这个值会被save进数据库,这里confirm对应的confirm_password没有被保存

# '''登录相关form'''
class LoginForm(BootstrpForm):
    username = forms.CharField(label='用户名', widget=forms.TextInput, required=True)
    password = forms.CharField(label='密码', widget=forms.PasswordInput(render_value=True), required=True)
    code = forms.CharField(label='验证码', widget=forms.TextInput, required=True)

    def clean_password(self):
        pwd = self.cleaned_data.get('password')
        return md5(pwd)

# 任务相关modelform
class TaskModelForm(BootstrapModelForm):
    class Meta:
        model = models.TaskInfo
        fields = ['level', 'title', 'detail', 'leader']
        widgets = {
            'title': forms.TextInput(attrs={'autocomplete': 'off'}),
            'detail': forms.TextInput(attrs={'autocomplete': 'off'}),
        }

# 订单相关modelform
class OrderModelForm(BootstrapModelForm):
    class Meta:
        model = models.Order
        exclude = ['oid','user']  # 排除oid，因为订单编号不是填的，是生成的