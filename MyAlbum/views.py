from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
from django.utils import timezone
from django.core.mail import send_mail
from MyAlbum import models, recognize, Tools
import os


# 跳转至主页
def index(request):
    return render(request, 'login.html')


# 注册
def register(request):
    if request.method == 'POST':
        _email_checkCode = request.POST.get('reg_chech_code')
        _username = request.POST.get('reg_username')
        _password = request.POST.get('reg_pwd')
        _email_addr = request.POST.get('reg_email_addr')
        message = {}
        try:
            check = models.Email_CheckCode.objects.get(email_addr=_email_addr)
            checkCode = check.check_code
            if _email_checkCode == checkCode:
                now = timezone.now()
                time = check.time
                if (now - time) > timezone.timedelta(minutes=10):
                    message = {'status': 'failed', 'reason': '验证码已过期，请重新获取'}
                else:
                    flag = True
                    try:
                        while flag:
                            account = Tools.get_CheckCode(n=8, alpha=False)
                            if not account == models.UserList.objects.filter(account=account)[0].account:
                                flag = False
                    except:
                        try:
                            user = models.UserList.objects.create(
                                account=int(account),
                                username=_username,
                                password=_password,
                                e_mail_address=_email_addr,
                                administration=0,
                                VIP=False
                            )
                            message = {'status': 'success', 'account': account}
                        except Exception as e:
                            message = {'status': 'failed', 'reason': '迷之错误'}
            else:
                message = {'status': 'failed', 'reason': '验证码错误'}
        except:
            message = {'status': 'failed', 'reason': '请先获取验证码'}

        finally:
            return JsonResponse(message)


# 处理前端登录请求
def login(request):
    if request.session.get('is_login', None):
        _account = request.POST.get('login_username')
        if _account == request.session.get('user_id', None):
            message = {'status': 'already'}
            return JsonResponse(message)

    if request.method == "POST":
        _account = request.POST.get('login_username')
        _pwd = request.POST.get('login_pwd')

        try:
            user = models.UserList.objects.filter(account=_account)
            if user[0].password == _pwd:
                request.session['is_login'] = True
                request.session['user_id'] = _account
                request.session['user_name'] = user[0].username
                message = {'status': 'success'}
            else:
                message = {'status': 'failed',
                           'reason': 'QaQ用户名或密码输入错误',
                           'account': _account,
                           }
            return JsonResponse(message)
        except Exception:
            message = {'status': 'failed',
                       'reason': 'QaQ用户名不存在',
                       'account': _account,
                       }
            return JsonResponse(message)


def change_to_homepage(request):
    return render(request, 'main.html')


# 判断后缀名是否为图片格式


def is_img(ext):
    ext = ext.lower()
    if ext in ['.jpg', '.png', '.jpeg', '.bmp']:
        return True
    else:
        return False


# 上传文件

def upload(request):
    if request.method == 'POST':
        albumID = request.POST.get('id', None)
        img = request.FILES.getlist('file')
        current_account = request.session.get('user_id')

        message = {}

        try:
            for i in img:
                pictureId = Tools.getPictureID(current_account)
                originalName = i.name
                bh_name = os.path.splitext(originalName)[-1]
                if not is_img(bh_name):
                    continue
                url = '/' + str(pictureId) + bh_name
                imageName = '%s%s' % (settings.MEDIA_ROOT, url)

                with open(imageName, 'wb') as imgWriter:
                    for i in i.chunks():
                        imgWriter.write(i)
                # 调用baiduAPI进行图像识别，返回list {'score': 0.838397, 'root': '非自然图像-设计图', 'keyword': '图表'}
                reco = recognize.shibie(imageName)

                piture = models.Storage.objects.create(
                    pictureID=pictureId,
                    pictureName=originalName,
                    path=imageName,
                    alterTime=timezone.now()
                )
                models.PitTag.objects.create(
                    pictureID=piture,
                    tag_1=str(reco[0]),
                    tag_2=str(reco[1]),
                    tag_3=str(reco[2])
                )
                models.User.objects.create(
                    account=models.UserList.objects.filter(account=current_account)[0],
                    pictureID=models.Storage.objects.filter(pictureID=pictureId)[0]
                )
                if albumID == '0':
                    Tools.collectPicture(current_account, pictureId)
                    message['albumID'] = []
                    if models.Album.objects.filter(account=current_account).exists():
                        album = models.Album.objects.filter(account=current_account).order_by('-alterTime')
                        for _album in album:
                            path = Tools.getPicturePath(_album.pictureID_id)
                            message['albumID'].append(_album.albumID)
                            message['albumID_' + str(_album.albumID)] = {
                                'albumName': _album.albumName,
                                'alterTime': _album.alterTime,
                                'cover': path
                            }
                        message['status'] = 'success'
                else:
                    models.AlbumStorage.objects.create(
                        albumID=models.Album.objects.get(albumID=int(albumID)),
                        pictureID=piture
                    )
                    album = models.Album.objects.get(albumID=albumID)
                    album.pictureID_id = pictureId
                    album.save()
                    message = Tools.getPictCollect(albumID)
                    if message:
                        message['status'] = 'success'
                    else:
                        message['status'] = 'no-picture'
                imgWriter.close()


        except Exception as writeE:
            message['status'] = 'failed'
        return JsonResponse(message)


# 获得某用户所有已存图片的名称和存储路径
def getAllPict(request):
    if request.session['is_login']:
        account = request.session['user_id']
        pict = []
        pictID = []
        message = {}
        try:
            pictList = models.Storage.objects.filter(user__account=account).order_by("-alterTime")
            for pic in pictList:
                path = pic.path.replace("\\", '\\\\')
                pictName = pic.pictureName
                pict_Name = '../static/upload/' + os.path.split(path)[-1]
                pict.append(pict_Name)
                pictID.append(pic.pictureID)
            # 获得成功之后返回数据给前端
            message['status'] = 'success'
            message['pict'] = pict
            message['pictID'] = pictID
            return JsonResponse(message)
        except Exception as e:
            # 若用户并未存储图片在此处理
            message['status'] = 'failed'
            return JsonResponse(message)
    return render(request, 'login.html')


# 获得验证码，发送验证邮件
def email_auth(request):
    check_Code = Tools.get_CheckCode(6, False)
    email_addr = request.POST.get('reg_email_addr')
    try:
        models.Email_CheckCode.objects.filter(email_addr=email_addr).delete()
    except:
        print('notexist')
    finally:
        models.Email_CheckCode.objects.create(email_addr=email_addr, check_code=check_Code, time=timezone.now())
        message = '感谢你注册本网站，您的验证码是：' + check_Code
        send_mail('云图集注册验证', message, settings.DEFAULT_FROM_EMAIL, [email_addr], fail_silently=True)
        return JsonResponse({'status': 'success'})


'''
页面初始化加载用户的设置封面和所有相册信息
'''


def getInfo_Album(request):
    if not request.session.get('is_login', None):
        return render(request, 'login.html')
    account = request.session['user_id']
    username = request.session['user_name']
    print(account)
    print(username)
    message = {}
    message['userName'] = username
    message['albumID'] = []
    info = Tools.getInfo(account)
    message['pict'] = Tools.getPicturePath(info['pict'])
    message['settings'] = info['settings']
    if models.Album.objects.filter(account=account).exists():
        album = models.Album.objects.filter(account=account).order_by('-alterTime')
        for _album in album:
            if not models.Storage.objects.filter(pictureID=_album.pictureID_id).exists():
                pictID = Tools.getPictCollect(_album.albumID)['pictID']
                path = Tools.getPicturePath(pictID[pictID.length - 1])
            else:
                path = Tools.getPicturePath(_album.pictureID_id)
            message['albumID'].append(_album.albumID)
            message['albumID_' + str(_album.albumID)] = {
                'albumName': _album.albumName,
                'alterTime': _album.alterTime,
                'cover': path
            }

        message['status'] = 'success'
    else:
        message['status'] = 'failed'
        message['reason'] = '用户还未创建相册'

    return JsonResponse(message)


# 退出登录 跳转至登录界面
def logout(request):
    if request.session.get('is_login', None):
        request.session['is_login'] = False
        request.session['user_id'] = None
        request.session['user_name'] = None
    return render(request, 'login.html')


'''
    创建相册的绑定事件，生成新相册的id和默认封面
'''


def addAlbum(request):
    message = {}
    message['albumID'] = []
    account = request.session['user_id']
    albumName = request.GET.get('name')
    if account is not None and albumName is not None:
        album = Tools.createAlbum(account, albumName, albumName)
        if models.Album.objects.filter(account=account).exists():
            album = models.Album.objects.filter(account=account).order_by('-alterTime')
            for _album in album:
                path = Tools.getPicturePath(_album.pictureID_id)
                message['albumID'].append(_album.albumID)
                message['albumID_' + str(_album.albumID)] = {
                    'albumName': _album.albumName,
                    'alterTime': _album.alterTime,
                    'cover': path
                }
        message['status'] = 'success'
    elif albumName is None:
        message = {'status': 'failed', 'reason': '相册名不能为空'}
    return JsonResponse(message)


'''
    点击相册的事件，跳转至相册内部显示相册所有图片
    如没有图片，则返回status no-picture
'''


def getPictByAlbum(request):
    messege = {}
    if request.session.get('is_login', None):
        albumID = request.GET.get('albumID')
        if albumID:

            messege = Tools.getPictCollect(albumID)
            if messege:
                messege['status'] = 'success'
            else:
                messege['status'] = 'no-picture'
        else:
            messege['status'] = 'failed'
        return JsonResponse(messege)
    else:
        return render(request, 'login.html')


# 跳转至个人信息界面
def changToInfo(request):
    if request.session.get('is_login', None):
        account = request.session.get('user_id', None)
        user = request.session.get('user_name', None)
        info = Tools.getInfo(account)
        pict = Tools.getPicturePath(info['pict'])
        messege = {'pict': pict, 'user': user, 'info': info['info'], 'email': info['email'],
                   'setting': info['settings']}
        return render(request, 'xinxi.html', {'message': messege})
    else:
        return render(request, 'login.html')


# 跳转至设置界面
def changToSetting(request):
    if request.session.get('is_login', None):
        account = request.session.get('user_id', None)
        user = request.session.get('user_name', None)
        info = Tools.getInfo(account)
        pict = Tools.getPicturePath(info['pict'])
        message = {'pict': pict, 'user': user, 'setting': info['settings']}
        return render(request, 'shezhi.html', {'message': message})
    else:
        return render(request, 'login.html')


# 跳转至反馈界面
def changToFankui(request):
    if request.session.get('is_login', None):
        account = request.session.get('user_id', None)
        user = request.session.get('user_name', None)
        info = Tools.getInfo(account)
        pict = Tools.getPicturePath(info['pict'])
        message = {'pict': pict, 'user': user, 'setting': info['settings']}
        return render(request, 'fankui.1.html', {'message': message})
    else:
        return render(request, 'login.html')


# 跳转至帮助界面
def changToHelp(request):
    if request.session.get('is_login', None):
        account = request.session.get('user_id', None)
        user = request.session.get('user_name', None)
        info = Tools.getInfo(account)
        pict = Tools.getPicturePath(info['pict'])
        message = {'pict': pict, 'user': user, 'setting': info['settings']}
        return render(request, 'bangzhu.html', {'message': message})
    else:
        return render(request, 'login.html')


# 用户修改设置的保存应用
def changSetting(request):
    if request.session.get('is_login', None):
        account = request.session.get('user_id', None)
        setting = str([request.GET.get('color1', None), request.GET.get('color2', None)])
        user = models.UserList.objects.filter(account=account)[0]
        user.settings = setting
        user.save()
        return render(request, 'shezhi.html', {'status': 'success'})
    else:
        return render(request, 'login.html')


'''
    用户反馈成功后跳转至返回成功界面
'''


def success(request):
    if request.session.get('is_login', None):
        account = request.session.get('user_id', None)
        user = request.session.get('user_name', None)
        info = Tools.getInfo(account)
        pict = Tools.getPicturePath(info['pict'])
        message = {'pict': pict, 'user': user, 'setting': info['settings']}
        return render(request, 'fankui.html', {'message': message})
    else:
        return render(request, 'login.html')


'''
    修改相册的tag的处理函数    
'''


def editTag(request):
    if request.session.get('is_login', None):
        account = request.session.get('user_id', None)
        albumID = request.GET.get('id', None)
        name = request.GET.get('name', None)
        album = models.Album.objects.get(albumID=int(albumID))

        message = {}
        if album.system == True:
            message['status'] = 'success'
            album.albumName = name
            album.save()
        else:
            message['status'] = 'failed'

        return JsonResponse(message)
    else:
        return render(request, 'login.html')


'''
删除相册，将相册内的所有图片状态转为已删除，移入回收站
'''


def deleteAlbum(request):
    if request.session.get('is_login', None):
        account = request.session.get('user_id', None)
        albumID = request.GET.get('id', None)
        if models.AlbumStorage.objects.filter(albumID=albumID).exists():
            pict = models.User.objects.filter(pictureID__albumstorage__albumID=albumID)
            for pic in pict:
                pic.is_delete = True
                pic.deleteTime = timezone.now()
                pic.save()
            models.AlbumStorage.objects.filter(albumID=albumID).delete()
        models.Album.objects.get(albumID=albumID).delete()
        message = {'status': 'success'}
        return JsonResponse(message)
    else:
        return render(request, 'login.html')


'''
在回收站以外删除图片
将该图片状态变为已删除
'''


def deletePhoto(request):
    if request.session.get('is_login', None):
        account = request.session.get('user_id', None)
        pictID = int(request.GET.get('id', None))
        try:
            if models.AlbumStorage.objects.filter(pictureID=pictID).exists():
                pict = models.User.objects.filter(pictureID=pictID)[0]
                pict.is_delete = True
                pict.deleteTime = timezone.now()
                pict.save()
        except Exception as e:
            print(e.args)
        message = {'status': 'success'}
        return JsonResponse(message)
    else:
        return render(request, 'login.html')


'''
跳转至回收站界面
'''


def recycle(request):
    if request.session.get('is_login', None):
        return render(request, 'recycle.html')
    else:
        return render(request, 'login.html')


'''
跳转到回收站后将该用户所有的已删除的图片信息返回给前端
'''


def showRecycle(request):
    if request.session.get('is_login', None):
        account = request.session.get('user_id', None)
        pictID = []
        pictPath = []
        message = {}
        if models.User.objects.filter(account=account, is_delete=True).exists():
            pict = models.User.objects.filter(account=account, is_delete=True)
            for pic in pict:
                pictID.append(pic.pictureID_id)
                path = Tools.getPicturePath(pic.pictureID_id)
                pictPath.append(path['path'])
            message['pictID'] = pictID
            message['pict'] = pictPath
            message['status'] = 'success'
        else:
            message['status'] = 'no-picture'
        return JsonResponse(message)
    else:
        return render(request, 'login.html')


'''
在回收站中删除图片，即将表中的所有记录删除并删除服务器中对应文件
'''


def deleteComplete(request):
    if request.session.get('is_login', None):
        account = request.session.get('user_id', None)
        pictID = request.GET.get('id', None)
        models.PitTag.objects.filter(pictureID=pictID).delete()
        models.Storage.objects.filter(pictureID=pictID).delete()
        return JsonResponse({'status': 'success'})
    else:
        return render(request, 'login.html')


'''
处理搜索的跳转函数，获得前端关键字content
调用Tools.search进行搜索
'''


def search(request, content):
    if request.session.get('is_login', None):
        account = request.session.get('user_id', None)
        keyword = content
        result = Tools.search(account, keyword)
        path = []
        for res in result['picture']:
            pictPath = Tools.getPicturePath(res)['path']
            path.append(pictPath)
        return render(request, 'searchresult.html', {'status': 'success', 'path': path, 'pictID': result})
    else:
        return render(request, 'login.html')
