import requests
import re 
import random
import time
import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cosershow.settings")
django.setup()
from coser.models import Coser, Photo

proxy = {'http': 'http://127.0.0.1:12639', 'https': 'http://127.0.0.1:12639'}
#外网代理

def printf(text):
    print("[%s] %s" % (time.strftime('%Y-%m-%d %H:%M:%S'), text))

def get_cookies():
    r = session.get("https://weibo.com/", allow_redirects=False, proxies=proxy)
    Ugrow_G0 = r.cookies['Ugrow-G0']
    LoginURL = r.headers.get('Location')
    LoginCookie = session.get(LoginURL, proxies=proxy).cookies['login']
    GenURL = "https://passport.weibo.com/visitor/genvisitor"
    Payload = {'cb': 'gen_callback',
                'fp': {"os": "1", "browser": "Gecko65,0,0,0", "fonts": "undefined", "screenInfo": "1920*1080*24","plugins": ""}}
    r = session.post(GenURL, data=Payload, cookies=dict(login=LoginCookie), proxies=proxy)
    tid = re.search(r'(?<="tid":").*?(?=")', r.text).group(0)
    LoginURL = "https://passport.weibo.com/visitor/visitor?"
    Payload = {'a': 'incarnate', 't': tid, 'w': '3', 'c': '100', 'gc': '',
                'cb': 'cross_domain', 'from': 'weibo', '_rand': str(random.uniform(0, 1))+str(random.uniform(999, 10000))}
    r = session.get(LoginURL, params=Payload, cookies=dict(login=LoginCookie, tid=tid+"__100"), proxies=proxy)
    try:
        sub = r.cookies['SUB']
        subp = r.cookies['SUBP']
        return dict(Ugrow_G0=Ugrow_G0, SUB=sub,  SUBP=subp)
    except KeyError:
        return {}

def download(imglist,uid, dirname=""):
    if not dirname:
        dirname = str(int(time.time()))
    if not os.path.isdir("coser/static/images/%s" % dirname):
        os.mkdir("coser/static/images/%s" % dirname)
    if not os.path.isdir("coser/static/img/%s" % uid):
        os.mkdir("coser/static/img/%s" % uid)
    printf("project:%s(%s)" % (dirname,len(imglist)))
    for filename in imglist:
        with open("coser/static/images/%s/%s.jpg" % (dirname, filename), mode='wb') as file:
            file.write(session.get("http://wx2.sinaimg.cn/large/%s.jpg" % filename, proxies=proxy).content)
        with open("coser/static/img/%s/%s.jpg" % (uid, filename), mode='wb') as file:
            file.write(session.get("http://wx2.sinaimg.cn/mw690/%s.jpg" % filename, proxies=proxy).content)
    
def getImage(uid):
    #访客接口只能浏览一页
    url = "https://weibo.com/p/%s/photos?type=photo" % uid

    #登录后接口（简化） 可以进行翻页
    #https://weibo.com/p/aj/album/loading?ajwvr=6&type=photo&owner_uid=20000&viewer_uid=20000&page_id=1005051868515735&page=2&ajax_call=1&since_id=4400509448638030_4367496142061900_20190819_-1

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36"
    }
    resp = session.get(url, proxies=proxy, headers = headers)
    pageHtml = re.findall(r'(?<=\().*(?=\))', resp.text)
    urllist = re.findall(r'mw1024%2F(.*?).(jpg|gif)', pageHtml[len(pageHtml)-1])
    imglist = []
    for url in urllist:
        #imglist.append("http://wx2.sinaimg.cn/large/%s." % url[1])
        #原图地址
        imglist.append(url[0])
    return (imglist) 

if __name__ == "__main__":
    
    while True:
        printf("开始执行任务")
        cookies = {}
        i=1
        while not cookies:
            printf("第%i次尝试获取访客状态" % i)
            session = requests.session()
            cookies = get_cookies()
            if cookies:
                printf("获取成功将获取照片墙")
            else:
                i=i+1
        coser = Coser.objects.filter()
        for c in coser:
            uid = c.uid #需要获取的微博Uid
            imglist = getImage(uid)
            querysetlist = [] 
            downloadlist = []
            for i in imglist:
                p = Photo.objects.filter(photoid=i)
                if len(p)==0:
                    querysetlist.append(Photo(uid=c.uid, photoid=i))
                    downloadlist.append(i)
            if len(querysetlist)>0:
                Photo.objects.bulk_create(querysetlist)
            if len(downloadlist)>0:
                download(downloadlist,c.uid,c.name)
        printf("本次任务结束")
        time.sleep(60*60)