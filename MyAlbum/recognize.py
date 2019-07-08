from aip import AipImageClassify


""" 你的 APPID AK SK """
APP_ID = '16664572'
API_KEY = 'fEFvj23fUyK3Sq5PGslY9ufx'
SECRET_KEY = 'IaBS3L4xGoHMqXllO40KWdFOyy1MMlgR'

client = AipImageClassify(APP_ID, API_KEY, SECRET_KEY)
""" 读取图片 """

def get_file_content(filepath):
    with open(filepath, 'rb') as fp:
        return fp.read()


def shibie (filename):
    get_file_content(filename)
    image = get_file_content(filename)
    """ 调用通用物体识别 """
    client.advancedGeneral(image)
    shili=client.advancedGeneral(image)
    i = 0
    list = []
    while i<=4:
        shilii = shili['result']
        shiliii = shilii[i]
        scores = shiliii['score']
        if scores > 0.3 or len(list) < 4:
            list.append(shiliii)
        i += 1
    return list




