import random, re, os, ast
from MyAlbum import models
from YunAlbum import settings


def get_CheckCode(n=6, alpha=True):
    s = ''  # 创建字符串变量,存储生成的验证码
    for i in range(n):  # 通过for循环控制验证码位数
        num = random.randint(0, 9)  # 生成随机数字0-9
        if alpha:  # 需要字母验证码,不用传参,如果不需要字母的,关键字alpha=False
            upper_alpha = chr(random.randint(65, 90))
            lower_alpha = chr(random.randint(97, 122))
            num = random.choice([num, upper_alpha, lower_alpha])
        s = s + str(num)
    return s


'''
为每一张图片进行tag处理，将其归类至相对应的相册
若该类相册不存在则创建
'''


def collectPicture(account, pictureid):
    pict = models.PitTag.objects.filter(pictureID=pictureid)[0]
    tag = ast.literal_eval(pict.tag_1)
    root = tag['root']
    keyword = tag['keyword']
    if root == '':
        tag = ast.literal_eval(pict.tag_2)
        root = tag['root']
        keyword = tag['keyword']
    ret = analyse_Tag(root, keyword)
    tag = ret['tag']
    cover = ret['cover']
    try:
        if not models.Album.objects.filter(account=account, tag_1=tag).exists():
            albumID = createAlbum(account, tag, tag, cover)
            models.AlbumStorage.objects.create(
                albumID=models.Album.objects.get(albumID=albumID),
                pictureID=models.Storage.objects.get(pictureID=pictureid)
            )
        else:
            album = models.Album.objects.filter(account=account, tag_1=tag)[0]
            models.AlbumStorage.objects.create(
                albumID=album,
                pictureID=models.Storage.objects.get(pictureID=pictureid)
            )
    except Exception as e:
        print(e.args)


'''
分析图片tag将其分为具体的类别
'''


def analyse_Tag(root, keyword):
    pattern = {
        'anime': '^.*动漫.*$',
        'animal': '^.*动物.*$',
        'cat': '^.*猫.*$',
        'dog': '^.*狗.*$',
        'bird': '^.*鸟.*$',
        'plant': '^.*植物.*$',
        'follower': '^.*花.*$',
        'creature': '^.*人物.*$',
        'public': '^.*公众人物.*$',
        'scene': '^.*风景.*$',
        'achitecture': '^.*建筑.*$',
        'vehicle': '^.*交通工具.*$',
        'car': '^.*车.*$'
    }
    result = {}

    if re.match(pattern['anime'], root):
        result['tag'] = '动漫'
        result['cover'] = 10002
    elif re.match(pattern['creature'], root):
        if re.match(pattern['public'], root):
            result['tag'] = '公众人物'
            result['cover'] = 10010
        else:
            result['tag'] = '人物'
            result['cover'] = 10006
    elif re.match(pattern['animal'], root):
        if re.match(pattern['dog'], root):
            result['tag'] = '狗'
            result['cover'] = 10007
        elif re.match(pattern['cat'], root):
            result['tag'] = '猫'
            result['cover'] = 10005
        elif re.match(pattern['bird'], root):
            result['tag'] = '鸟'
            result['cover'] = 10003
        else:
            result['tag'] = '动物'
            result['cover'] = 10001
    elif re.match(pattern['plant'], root):
        if re.match(pattern['follower'], root):
            result['tag'] = '花'
            result['cover'] = 10008
        else:
            result['tag'] = '植物'
            result['cover'] = 10009
    elif re.match(pattern['achitecture'], root):
        result['tag'] = '建筑'
        result['cover'] = 10000
    elif re.match(pattern['vehicle'], root):
        if re.match(pattern['car'], keyword):
            result['tag'] = '车'
            result['cover'] = 10004
        else:
            result['tag'] = '交通工具'
            result['cover'] = 10012
    elif re.match(pattern['scene'], root):
        result['tag'] = '风景'
        result['cover'] = 10011
    else:
        result['tag'] = '其他'
        result['cover'] = 10013

    return result


'''
为用户名为account的用户创建名字为albumName的相册并返回其albumID
并指定相册的tag
'''


def createAlbum(account, albumName, tag, pictureid=0):
    albumID = getAlbumID(account)
    picture = models.Storage.objects.get(pictureID=pictureid)
    models.Album.objects.create(
        albumName=albumName,
        albumID=albumID,
        tag_1=tag,
        account=models.UserList.objects.get(account=account),
        pictureID=picture,
        custom_Tag_1=None
    )
    path = settings.STATIC_URL + 'img/' + os.path.split(picture.path)[-1]
    return albumID


'''
获取account用户下的相册id的最大值加一
'''


def getAlbumID(account):
    flag = 1
    album = models.Album.objects.filter(account=account).order_by('-albumID')
    if not album:
        flag = 1
    else:
        albumTop = str(album[0].albumID)
        pattern = re.compile('^' + account + '(\d+)$')
        flag = pattern.findall(albumTop)
        flag = int(flag[0]) + 1
    try:
        albumID = int(str(account) + str(flag))
    except Exception as e:
        print(e.args)
    return albumID


'''
获得用户的设置头像昵称等基本信息
'''


def getInfo(account):
    user = models.UserList.objects.filter(account=account)[0]
    info = {}
    info['pict'] = user.pictureID
    info['settings'] = user.settings
    info['info'] = user.info
    info['email'] = user.e_mail_address
    return info


'''
通过pictureid查找图片的存储路径和图片本名等
'''


def getPicturePath(pictureid):
    pict = models.Storage.objects.get(pictureID=pictureid)
    path = settings.STATIC_URL + 'upload/' + os.path.split(pict.path)[-1]
    return {'path': path, 'pict_name': pict.pictureName}


'''
getPictCollect 
通过albumid查询其内包含的所有图片的path id name
'''


def getPictCollect(albumID):
    message = {}
    if models.AlbumStorage.objects.filter(albumID=albumID).exists():
        pict = models.AlbumStorage.objects.filter(albumID=albumID)
        message['pictID'] = []
        for _pict in pict:
            if models.User.objects.filter(pictureID=_pict.pictureID)[0].is_delete:
                continue
            else:
                message['pictID'].append(_pict.pictureID_id)
                message[_pict.pictureID_id] = getPicturePath(_pict.pictureID_id)
    return message


def getPictureID(account):
    flag = 1

    if not models.User.objects.filter(account=account).exists():
        flag = 1
    else:
        pict = models.User.objects.filter(account=account).order_by('-pictureID')
        pictTop = str(pict[0].pictureID_id)
        pattern = re.compile('^' + account + '(\d+)$')
        flag = pattern.findall(pictTop)
        flag = int(flag[0]) + 1

    pictID = int(str(account) + str(flag))

    return pictID

def search(account, keyword):
    pattern = re.compile('^.*' + keyword + '.*$')
    searchField = {}
    searchField['Album'] = []
    try:
        album = models.Album.objects.filter(account=account)
        for al in album:
           if pattern.match(al.tag_1) or pattern.match(al.albumName):
               searchField['Album'].append(al.albumID)
        searchField['picture'] = []
        for al in searchField['Album']:
            if models.AlbumStorage.objects.filter(albumID=al).exists():
                pict = models.AlbumStorage.objects.filter(albumID=al)
                for pic in pict:
                    searchField['picture'].append(pic.pictureID_id)
    except Exception as e:
        print(e.args)

    return searchField

