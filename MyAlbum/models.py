from django.db import models

# Create your models here.

'''
UserList
包含：username用户名，5-16字符
account账号 字符串类型 自动生成的账号
password密码 8位以上
'''


class UserList(models.Model):
    username = models.CharField(max_length=16)
    account = models.CharField(max_length=10, primary_key=True)
    password = models.CharField(max_length=25)


'''
Storage table
pictureID 为每个picture获取唯一编号
pictureName picture 的原文件名 
path 文件的云端存储路径
'''


class Storage(models.Model):
    pictureID = models.IntegerField(null=False, primary_key=True)
    pictureName = models.CharField(max_length=255, null=False)
    path = models.CharField(max_length=255, null=False)


'''
User表
account 字符串 引用User_list表中的account
Storage.pictureID 
VIP 该用户身份
'''


class User(models.Model):
    account = models.ForeignKey(UserList, on_delete=models.CASCADE)
    pictureID = models.ForeignKey(Storage, on_delete=models.CASCADE)
    VIP = models.BooleanField()


'''
PitTag 图片识别出的标签
Storage.pictureID
tag_1 字符串 识别出的图片的标签 允许为空
tag_2
tag_3
自定义的用户标签
custom_Tag_1
custom_Tag_2
custom_Tag_3
'''


class PitTag(models.Model):
    pictureID = models.ForeignKey(Storage, null=False, on_delete=models.CASCADE)
    tag_1 = models.CharField(max_length=30)
    tag_2 = models.CharField(max_length=30)
    tag_3 = models.CharField(max_length=30)
    custom_Tag_1 = models.CharField(max_length=30)
    custom_Tag_2 = models.CharField(max_length=30)
    custom_Tag_3 = models.CharField(max_length=30)


'''
Album
UserList.account
albumID
albumName
'''


class Album(models.Model):
    albumID = models.CharField(max_length=20, primary_key=True)
    albumName = models.CharField(max_length=255, null=False)
    account = models.ForeignKey(UserList, null=False, on_delete=models.CASCADE)


'''
AlbumTag 给对应相册加Tag
tag_1 字符串 识别出的图片的标签 允许为空
tag_2
tag_3
自定义相册的用户标签
custom_Tag_1
custom_Tag_2
custom_Tag_3
'''


class AlbumTag(models.Model):
    albumID = models.ForeignKey(Album, on_delete=models.CASCADE)
    tag_1 = models.CharField(max_length=30)
    tag_2 = models.CharField(max_length=30)
    tag_3 = models.CharField(max_length=30)
    custom_Tag_1 = models.CharField(max_length=30)
    custom_Tag_2 = models.CharField(max_length=30)
    custom_Tag_3 = models.CharField(max_length=30)