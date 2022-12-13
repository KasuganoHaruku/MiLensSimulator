from pickletools import genops
from random import weibullvariate
from string import hexdigits
import tkinter
import os
from tkinter import *
import tkinter.filedialog
import exifread
from PIL import ImageFont, Image, ImageDraw
import getpass
import sys

gps=0
savepath=sys.path[0]
sourcepath=savepath+"/resource"
window=Tk()
window.title=("Camera")
lb = Label(window,text='')
lb.grid(column=1, row=0)
lb2 = Label(window,text='')
lb2.grid(column=0, row=1)
lb3 = Label(window,text='')
lb3.grid(column=1, row=1)

def clicked():
    filename = tkinter.filedialog.askopenfilename()
    img_path=filename
    global image
    image=Image.open(img_path)
    global w
    w=image.width
    global h
    h=image.height
    lb2.config(text=image.format)
    lb3.config(text=image.size)
    lb.config(text =filename)
    f = open(img_path, 'rb')
    global tags
    tags = exifread.process_file(f)
    for tag in tags.keys():
        print("Key: {0}, value {1}".format(tag, tags[tag]))
    global model
    model=str(tags['Image Model'])
    global time
    time=str(tags['Image DateTime'])
    global infos
    infos=str(float(eval(str(tags['EXIF FocalLength']))))+'mm f/'+str(float(eval(str(tags['EXIF FNumber']))))+' '+str(tags['EXIF ExposureTime'])+' ISO'+str(tags['EXIF ISOSpeedRatings'])
    jing=str(tags['GPS GPSLongitude'])
    if jing!=0:
        global gps
        gps=1
        listj = jing[1: -1].replace("/", ",").split(",")
        wei=str(tags['GPS GPSLatitude'])
        listw= wei[1: -1].replace("/", ",").split(",")
        jfen=float(listj[2])/float(listj[3])
        wfen=float(listw[2])/float(listw[3])
        wtext=str(listw[0])+"°"+str(listw[1])+'\''+str(round(jfen))+'\"'+str(tags['GPS GPSLatitudeRef'])
        jtext=str(listj[0])+"°"+str(listj[1])+'\''+str(round(wfen))+'\"'+str(tags['GPS GPSLongitudeRef'])
        global jingwei
        jingwei=wtext+' '+jtext
        
btn = Button(window, text="File", command=clicked)
btn.grid(column=0, row=0)

def leica():
    global maker
    maker=leica
    lb4.config(text='Leica')
    global logo
    logo=Image.open(sourcepath+'/leica.png')    
def canon():
    global maker
    maker=canon
    lb4.config(text='Canon')
    global logo
    logo=Image.open(sourcepath+'/canon.png')    
def nikon():
    global maker
    maker=nikon
    lb4.config(text='Nikon')
    global logo
    logo=Image.open(sourcepath+'/nikon.png')
def hass():
    global maker
    maker=hass
    lb4.config(text='Hasselblad')
    global logo
    logo=Image.open(sourcepath+'/hasselblad.png')
def apple():
    global maker
    maker=apple
    lb4.config(text='Apple')
    global logo
    logo=Image.open(sourcepath+'/apple.png')
def op():
    global maker
    maker=op
    lb4.config(text='OnePlus')
    global logo
    logo=Image.open(sourcepath+'/oneplus.jpg')
def fuji():
    global maker
    maker=fuji
    lb4.config(text='Fuji')
    global logo
    logo=Image.open(sourcepath+'/fuji.png')

leica = Button(window, text="Leica", command=leica)
leica.grid(column=0, row=2)
canon = Button(window, text="Canon", command=canon)
canon.grid(column=1, row=2)
nikon = Button(window, text="Nikon", command=nikon)
nikon.grid(column=2, row=2)
hass = Button(window, text="Hasselblad", command=hass)
hass.grid(column=3, row=2)
pg = Button(window, text="Apple", command=apple)
pg.grid(column=4, row=2)
fuji = Button(window, text="Fuji", command=fuji)
fuji.grid(column=5, row=2)
op = Button(window, text="OnePlus", command=op)
op.grid(column=6, row=2)
lb4 = Label(window,text='')
lb4.grid(column=0, row=3)

def process():
    hp=round(h*0.13)
    fh=round(hp/5.2)
    fx=round(w/33.75)
    fy=round(hp/2.6-fh)
    fh1=round(hp/6.35)
    fx1=fx
    fy1=round(hp/1.9)
    fh2=fh
    fx2=0
    fy2=fy
    fh3=fh1
    fx3=0
    fy3=fy1
    lgh=round(hp/1.7)
    lgx=0
    lgy=fy
    leica = Image.new('RGB',(w,hp),(255,255,255))
    draw = ImageDraw.Draw(leica)
    username=getpass.getuser()
    font = ImageFont.truetype('C:/Users/'+username+'/AppData/Local/Microsoft/Windows/Fonts/MiSans-Demibold.ttf', size=fh)
    font1 = ImageFont.truetype('C:/Users/'+username+'/AppData/Local/Microsoft/Windows/Fonts/MiSans-Regular.ttf', size=fh1)
    font2 = ImageFont.truetype('C:/Users/'+username+'/AppData/Local/Microsoft/Windows/Fonts/MiSans-Demibold.ttf', size=fh2)
    font3 = ImageFont.truetype('C:/Users/'+username+'/AppData/Local/Microsoft/Windows/Fonts/MiSans-Regular.ttf', size=fh3)
    wt, ht = draw.textsize(infos,font=font2)
    fx2=w-fx-wt
    fx3=fx2
    draw.text(xy=(fx, fy), text=model, fill=(0, 0, 0), font=font)
    draw.text(xy=(fx1, fy1), text=time, fill=(78, 78, 78), font=font1)
    draw.text(xy=(fx2, fy2), text=infos, fill=(0, 0, 0), font=font2)
    draw.rectangle((fx2-round(lgh/2.3),fy1+2*fh1,fx2-round(lgh/2.3)+5,fy2),fill=(172,172,172))
    if gps==1:
        draw.text(xy=(fx3, fy3), text=jingwei, fill=(78, 78, 78), font=font3)
    if maker==fuji:
        lghx=round(lgh*5.7)
        logo2=logo.resize((lghx,lgh))
    elif maker==canon:
        lghx=round(lgh*4.1)
        logo2=logo.resize((lghx,lgh))
    elif maker==hass:
        lghx=round(lgh*3.75)
        logo2=logo.resize((lghx,lgh))
    else:
        lghx=lgh
        logo2=logo.resize((lgh,lgh))
    lgx=fx2-round(lgh/2.3)*2-lghx
    leica.paste(logo2,(lgx,lgy))
    final = Image.new('RGB', (w,h+hp))
    final.paste(image, (0, 0))
    final.paste(leica, (0, h))
    final.save(savepath + "/final.jpg")
pro = Button(window, text="Process", command=process)
pro.grid(column=0, row=4)
window.mainloop()