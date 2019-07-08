from django.db import models
from datetime import date
from django.utils import timezone
import pymysql

# Create your models here.

'''
UserList
包含：username用户名，5-16字符
account账号 字符串类型 自动生成的账号
password密码 8位以上
administration 是否为管理员
email 邮箱地址
VIP 是否为VIP
registerTime 注册时间
'''


class UserList(models.Model):
    username = models.CharField(max_length=16)
    account = models.CharField(max_length=10, primary_key=True)
    password = models.CharField(max_length=25)
    administration = models.BooleanField(max_length=1)
    e_mail_address = models.CharField(max_length=40)
    VIP = models.BooleanField()
    registerTime = models.DateField(default=date.today())


'''
Storage table
pictureID 为每个picture获取唯一编号
pictureName picture 的原文件名 
path 文件的云端存储路径
altertime 图片的修改时间
'''


class Storage(models.Model):
    pictureID = models.IntegerField(null=False, primary_key=True)
    pictureName = models.CharField(max_length=255, null=False)
    path = models.CharField(max_length=255, null=False)
    alterTime = models.DateTimeField(default=timezone.now())


'''
User表 图片与用户的关系
account 字符串 引用User_list表中的account
Storage.pictureID 
'''


class User(models.Model):
    account = models.ForeignKey(UserList, on_delete=models.CASCADE)
    pictureID = models.ForeignKey(Storage, on_delete=models.CASCADE)



'''
PitTag 图片识别出的标签
Storage.pictureID
tag_1 字符串 识别出的图片的标签 允许为空
tag_2
tag_3
自定义的用户标签
custom_Tag_1
'''


class PitTag(models.Model):
    pictureID = models.ForeignKey(Storage, null=False, on_delete=models.CASCADE)
    tag_1 = models.CharField(max_length=100)
    tag_2 = models.CharField(max_length=100)
    tag_3 = models.CharField(max_length=100)
    custom_Tag_1 = models.CharField(max_length=20, null=True)


'''
Album
UserList.account
albumID
albumName
pictureID cover
'''


class Album(models.Model):
    albumID = models.CharField(max_length=20, primary_key=True)
    albumName = models.CharField(max_length=255, null=False)
    account = models.ForeignKey(UserList, null=False, on_delete=models.CASCADE)
    alterTime = models.DateTimeField(default=timezone.now())
    pictureID = models.ForeignKey(Storage, on_delete=models.CASCADE)
    tag_1 = models.CharField(max_length=100)
    custom_Tag_1 = models.CharField(max_length=20, null=True)







'''
存储图片与相册的所属关系
'''

class AlbumStorage(models.Model):
    albumID = models.ForeignKey(Album, on_delete=models.CASCADE)
    pictureID = models.ForeignKey(Storage, on_delete=models.CASCADE)



class Email_CheckCode(models.Model):
    email_addr = models.EmailField()
    check_code = models.CharField(max_length=6, null=True)
    time = models.DateTimeField(default=timezone.now())
