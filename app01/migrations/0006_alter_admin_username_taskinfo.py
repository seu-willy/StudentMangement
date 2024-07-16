# Generated by Django 5.0.6 on 2024-07-01 06:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0005_admin_alter_preetynum_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='admin',
            name='username',
            field=models.CharField(max_length=64, unique=True, verbose_name='账号'),
        ),
        migrations.CreateModel(
            name='TaskInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.SmallIntegerField(choices=[(1, '紧急'), (2, '重要'), (3, '一般'), (4, '临时')], default=4, verbose_name='任务等级')),
                ('title', models.CharField(max_length=64, verbose_name='标题')),
                ('detail', models.TextField(max_length=1024, verbose_name='任务详情')),
                ('leader', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.admin', verbose_name='负责人')),
            ],
        ),
    ]
