from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from django.conf import settings

from django.utils import timezone
from django.core.mail import send_mail
from MyAlbum import models,recognize,Tools
import os,json
# Create your views here.


# 跳转至主页
def index(request):
    '''if request.session.get('is_login', None):
        return redirect('change_to_homepage/getAlbum/')'''
    return render(request, 'login.html')


# 跳转至注册界面
# def change_to_register(request):
#   return render(request, ".html")

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
                    message = {'status':'failed', 'reason':'验证码已过期，请重新获取'}
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
                message = {'status':'failed', 'reason': '验证码错误'}
        except:
            message = {'status':'failed', 'reason': '请先获取验证码'}

        finally:
            return JsonResponse(message)

# 处理前端登录请求
def login(request):

    if request.session.get('is_login', None):
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


def changToUpload(request):
    return render(request, 'testFileUpload.html')
# 上传文件

def upload(request):
    if request.method == 'POST':
        img = request.FILES.getlist('upload_input')
        current_account = request.session.get('user_id')
        pictureId = 0
        try:
            pictureId = models.Storage.objects.all().order_by('-pictureID')[0].pictureID + 1
        except Exception as e:
            print(e)
            print('图片ID获取失败')
        message = {}

        try:
            for i in img:
                originalName = i.name
                bh_name = os.path.splitext(originalName)[-1]
                if not is_img(bh_name):
                    message['fail'] = originalName
                    continue
                url = '/' + current_account + '-' + str(pictureId) + bh_name
                imageName = '%s%s' % (settings.MEDIA_ROOT, url)

                with open(imageName, 'wb') as imgWriter:
                    for i in i.chunks():
                        imgWriter.write(i)
                # 调用baiduAPI进行图像识别，返回list {'score': 0.838397, 'root': '非自然图像-设计图', 'keyword': '图表'}
                reco = recognize.shibie(imageName)

                piture = models.Storage.objects.create(
                    pictureID=pictureId,
                    pictureName=originalName,
                    path=imageName
                )
                pitTag = models.PitTag.objects.create(
                    pictureID=piture,
                    tag_1=str(reco[0]),
                    tag_2=str(reco[1]),
                    tag_3=str(reco[2])
                )
                user = models.User.objects.create(
                    account=models.UserList.objects.filter(account=current_account)[0],
                    pictureID=models.Storage.objects.filter(pictureID=pictureId)[0]
                 )



                pictureId += 1
                imgWriter.close()
            return redirect('/showPict')

        except Exception as writeE:
                print(writeE)
                return render(request, 'hello.html', {'message': message})

#获得某用户所有已存图片的名称和存储路径
def getAllPict(request):
    if request.session['is_login']:
        user = request.session['user_id']
        pict = []
        try:
            pictList = models.User.objects.filter(account=user)

            for pic in pictList:
                stor = models.Storage.objects.filter(pictureID=pic.pictureID.pictureID)
                path = stor[0].path.replace("\\", '\\\\')
                pictName = stor[0].pictureName
                pict_Name = os.path.split(path)[-1]

                pict.append(pict_Name)
        #获得成功之后返回数据给前端
            return render(request, 'hello.html',  {'p': pict})
        except Exception as e:
            #若用户并未存储图片在此处理
            return HttpResponse('未存储图片')
    return HttpResponse('获得数据失败')

def email_auth(request):
    check_Code = Tools.get_CheckCode(6, False)
    email_addr = request.POST.get('reg_email_addr')
    try:
        models.Email_CheckCode.objects.filter(email_addr=email_addr).delete()
    except:
        print('notexist')
    finally:
        models.Email_CheckCode.objects.create(email_addr=email_addr, check_code=check_Code,time=timezone.now())
        message = '感谢你注册本网站，您的验证码是：' + check_Code
        send_mail('云图集注册验证', message, settings.DEFAULT_FROM_EMAIL, [email_addr], fail_silently=True)
        return JsonResponse({'status': 'success'})


def getAlbum(request):
    account = request.session['user_id']
    message = {}

    message['albumID'] = []
    if models.Album.objects.filter(account=account).exists():
        album = models.Album.objects.filter(account=account).order_by('-alterTime')
        for _album in album:
            cover = models.Storage.objects.filter(pictureID=_album.pictureID_id)[0]
            path =settings.STATIC_URL + 'img/' + os.path.split(cover.path)[-1]
            message['albumID'].append(_album.albumID)
            message['albumID_' + _album.albumID] = {
                'albumName': _album.albumName,
                'alterTime': _album.alterTime,
                'cover': path
            }
        message['status'] = 'success'
    else:
        message = {'status': 'failed', 'reason': 'null'}

    return JsonResponse(message)


def logout(request):
    request.session['is_login'] = False
    return JsonResponse({'status': 'success'})

def addAlbum(request):
    message = {}
    account = request.session['user_id']
    albumName = request.GET.get('name')
    if account is not None and albumName is not None:
        album = Tools.createAlbum(account, albumName, albumName)
        message = {'status': 'success', 'albumID': album['albumID'], 'cover': album['cover']}
    elif albumName is None:
        message = {'status': 'failed', 'reason': '相册名不能为空'}
    return JsonResponse(message)

def changToInfo(request):
    return render(request, 'xinxi.html')


def changToSetting(request):
    return render(request, 'shezhi.html')


def changToFankui(request):
    return render(request, 'fankui.1.html')


def changToHelp(request):
    return render(request, 'bangzhu.html')


