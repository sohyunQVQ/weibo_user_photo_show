from django.shortcuts import render
from coser.models import Coser, Photo
from datetime import datetime, timezone
# Create your views here.

def index(request):
    def getSecond(elem):
        return elem['time']
    showcoser = []
    coser = Coser.objects.filter()
    for c in coser:
        coserp={}
        coserp['uid'] = c.uid
        coserp['coser'] = c.name
        try:
            img = Photo.objects.filter(uid=c.uid).order_by('-time')[0]
        except IndexError:
            continue
        coserp['imgid'] = img.photoid
        coserp['time'] = img.time.strftime('%Y-%m-%d %H:%M')
        showcoser.append(coserp)
    showcoser.sort(key=getSecond, reverse=True)
    return render(request, "show.html", {'coser': showcoser})

def coser(request, uid):
    showcoser = []
    coser = Coser.objects.filter(uid=uid)[0]
    imgs = Photo.objects.filter(uid=uid).order_by('-time')
    for img in imgs:
        coserp={}
        coserp['coser'] = coser.name
        coserp['imgid'] = img.photoid
        coserp['time'] = img.time.strftime('%Y-%m-%d %H:%M')
        coserp['puid'] = coser.uid
        showcoser.append(coserp)
    return render(request, "show.html", {'coser': showcoser})

def search(request):
    search = request.POST['search']
    if search:
        showcoser = []
        coser = Coser.objects.filter(name__contains=search)
        for c in coser:
            coserp={}
            coserp['uid'] = c.uid
            coserp['coser'] = c.name
            img = Photo.objects.filter(uid=c.uid).order_by('-time')[0]
            coserp['imgid'] = img.photoid
            coserp['time'] = img.time.strftime('%Y-%m-%d %H:%M')
            showcoser.append(coserp)
        return render(request, "show.html", {'coser': showcoser})