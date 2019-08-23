# 微博用户照片墙爬取

### 第一个终端
```Shell
pip install django
pip install requests
cd weibo_user_photo_show
python manage.py migrate
python createsuperuser
python manage.py runserver
```

### 第二个终端
```Shell
cd weibo_user_photo_show
python getimage.py
```

###所用库版本
```
    django=2.2.3
    python=3.7.4
    requests=2.22.0
```

###使用方法
```
    当完成第一个终端命令后打开http://站点/admin
    点入Coser的模型添加对应用户的微博名(别名), UID(10050521*******)
    添加完成后在第二个终端运行命令开始爬取
    getimage.py内自带每小时运行执行爬取, 可在代码内修改
    关键：：：
    请自行删除getimage.py内的proxy代理才能正常爬取！
```