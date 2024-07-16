from django.db import models


class Admin(models.Model):
    username = models.CharField(verbose_name="账号", max_length=64, unique=True)
    password = models.CharField(verbose_name="密码", max_length=64)
    def __str__(self):
        return self.username

class Department(models.Model):
    '''部门表'''
    title = models.CharField(verbose_name='部门名称', max_length=64)
    def __str__(self):
        return self.title


class UserInfo(models.Model):
    '''员工表'''
    name = models.CharField(verbose_name='姓名', max_length=32)
    password = models.CharField(verbose_name='密码', max_length=64)
    age = models.IntegerField(verbose_name='年龄')
    account = models.DecimalField(verbose_name='账户余额', max_digits=10, decimal_places=2, default=0)
    create_time = models.DateField(verbose_name='入职时间')
    depart = models.ForeignKey(verbose_name='所属部门', to='Department', to_field='id',
                               on_delete=models.CASCADE)  # 关联表删除，自己删除
    # depart = models.ForeignKey(to='Department', to_field='id', on_delete=models.SET_NULL, null=True, blank=True)  # 关联表删除，自己为空
    gender_choices = (
        (1, '男'),
        (2, '女')
    )
    gender = models.SmallIntegerField(verbose_name='性别', choices=gender_choices)
    def __str__(self):
        return self.name

class PreetyNum(models.Model):
    '''靓号表'''
    mobile = models.CharField(verbose_name='靓号号码', max_length=32)
    price = models.IntegerField(verbose_name='价格', default=0)
    level_choices = (
        (1, '1级'),
        (2, '2级'),
        (3, '3级'),
        (4, '4级'),
    )
    level = models.SmallIntegerField(verbose_name='等级', choices=level_choices, default=1)
    status_choices = (
        (1, '已占用'),
        (2, '未使用')
    )
    status = models.IntegerField(verbose_name='状态', choices=status_choices, default=2)


class TaskInfo(models.Model):
    level_choices = (
        (1, "紧急"),
        (2, "重要"),
        (3, "一般"),
        (4, "临时")
    )
    level = models.SmallIntegerField(verbose_name="任务等级", choices=level_choices, default=4)
    title = models.CharField(verbose_name="标题", max_length=64)
    detail = models.TextField(verbose_name="任务详情", max_length=1024)
    leader = models.ForeignKey(verbose_name="负责人", to='Admin', to_field="id", on_delete=models.CASCADE)

class Order(models.Model):
    oid = models.CharField(verbose_name="订单编号", max_length=128, unique=True)
    title = models.CharField(verbose_name="商品名称", max_length=64)
    price = models.IntegerField(verbose_name="商品价格")
    status_choices = (
        (1,"待支付"),
        (2,"已支付")
    )
    status = models.SmallIntegerField(verbose_name="商品状态", choices=status_choices, default=1)
    user = models.ForeignKey(verbose_name="用户", to=Admin, to_field="id", on_delete=models.CASCADE)

class Boss(models.Model):
    name = models.CharField(verbose_name="姓名", max_length=64)
    age = models.SmallIntegerField(verbose_name="年龄")
    img= models.CharField(verbose_name="头像", max_length=128)

class City(models.Model):
    # FileField, 在数据库中存储依然是路径
    name = models.CharField(verbose_name="名称", max_length=64)
    num = models.IntegerField(verbose_name="人口")
    img = models.FileField(verbose_name="Logo", max_length=64, upload_to='city')  # 文件需要指定一个media下的目录