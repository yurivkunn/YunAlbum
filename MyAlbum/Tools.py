import random,re,os
from MyAlbum import models
from YunAlbum import settings

def get_CheckCode(n=6,alpha=True):
    s = '' # 创建字符串变量,存储生成的验证码
    for i in range(n):  # 通过for循环控制验证码位数
        num = random.randint(0,9)  # 生成随机数字0-9
        if alpha: # 需要字母验证码,不用传参,如果不需要字母的,关键字alpha=False
            upper_alpha = chr(random.randint(65,90))
            lower_alpha = chr(random.randint(97,122))
            num = random.choice([num,upper_alpha,lower_alpha])
        s = s + str(num)
    return s

'''
为每一张图片进行tag处理，将其归类至相对应的相册
若该类相册不存在则创建
'''
def collectPicture(account, pictureid):
    if models.User.objects.filter(account=account).exists() and pictureid == models.User.objects.filter(account=account)[0].pictureID:
        pict = models.PitTag.objects.filter(pictureID=pictureid)[0]
        root = pict.tag_1['root']
        keyword = pict.tag_1['keyword']
        if root == '':
            root = pict.tag_2['root']
            keyword = pict.tag_2['keyword']
        ret = analyse_Tag(root, keyword)

        if not models.Album.objects.filter(account=account, tag=ret).exists():
            createAlbum(account, ret, ret)
        else:
            album = models.Album.objects.filter(account=account, tag=ret)[0]
            models.AlbumStorage.objects.create(albumID=album.albumID, pictureID=pictureid)



'''
分析图片tag将其分为具体的类别
'''


def analyse_Tag(root, keyword):
    pattern = {
        'anime': '^.*动漫.*$',
        'animal': '^.*动物.*$',
        'dog': '^.*猫.*$',
        'cat': '^.*狗.*$',
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
    result = ''

    if re.match(pattern['anime'], root):
        result = '动漫'
    elif re.match(pattern['creature'], root):
        if re.match(pattern['public'], root):
            result = '公众人物'
        else:
            result = '人物'
    elif re.match(pattern['animal'], root):
        if re.match(pattern['dog'], root):
            result = '狗'
        elif re.match(pattern['cat'], root):
            result = '猫'
        elif re.match(pattern['bird'], root):
            result = '鸟'
        else:
            result = '动物'
    elif re.match(pattern['plant'], root):
        if re.match(pattern['follower'], root):
            result = '花'
        else:
            result = '植物'
    elif re.match(pattern['achitecture'], root):
        result = '建筑'
    elif re.match(pattern['vehicle'], root):
        if re.match(pattern['car'], keyword):
            result = '车'
        else:
            result = '交通工具'
    elif re.match(pattern['scene'], root):
        result = '风景'
    else:
        result = '其他'

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
    return {'albumID': albumID, 'cover': path}


'''
获取account用户下的相册id的最大值加一
'''
def getAlbumID(account):
    flag = 1
    album = models.Album.objects.filter(account=account).order_by('-albumID')
    if not album:
        flag = 1
    else:
        albumTop = album[0].albumID
        pattern = re.compile('^' + account + '(\d+)$')
        flag = pattern.findall(albumTop)
        flag = int(flag[0]) + 1
    try:
        albumID = int(str(account) + str(flag))
    except Exception as e:
        print(e.args)
    return albumID
