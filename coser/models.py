from django.db import models

# Create your models here.
# 两个model 一个是存放Coser的ID 另外个是抓取的记录

class Coser(models.Model):
    name = models.CharField(max_length=32)
    uid = models.CharField(max_length=16)
    def __str__(self):
        return self.name

class Photo(models.Model):
    uid = models.CharField(max_length=16)
    photoid = models.CharField(max_length=32)
    time = models.DateTimeField(auto_now_add=True)