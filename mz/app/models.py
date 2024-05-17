from django.db import models
from django.contrib.auth.models import User
from PIL import Image, ImageDraw, ImageFont

from PIL.ExifTags import TAGS
import arabic_reshaper
import bidi.algorithm
import os

# Create your models here.


def get_exif_data(image_path):
    # فتح الصورة
    image = Image.open(image_path)
    exif_data = image._getexif()
    if exif_data is None:
        return None
    exif_data = {TAGS[key]: value for key, value in exif_data.items()}
    return exif_data

def is_taken_with_phone(image_path):
    exif_data = get_exif_data(image_path)
    if exif_data == None:
        return False
    return 'Model' in exif_data

if os.path.expanduser("~") == 'C:\\Users\\H1720':
    thePath = r"C:\Users\H1720\Documents\mz-engineering\mzengineering\static\fonts\arial.ttf"
    theLogo = r"C:\Users\H1720\Documents\mz-engineering\mzengineering\static\img\logo.png"
else:
    thePath = "/home/assays/mzengineering/mz/static/fonts/arial.ttf"
    theLogo = "/home/assays/mzengineering/mz/static/img/logo.png"

class UserTable(models.Model):
    main_user       = models.ForeignKey(User,on_delete=models.CASCADE)
    consultant_name = models.CharField(max_length=50)
    job_number      = models.CharField(max_length=50)
    phone           = models.CharField(max_length=13)
    class Users(models.TextChoices):
        ADMIN = "admin"
        USER  = "user"
    user_role       = models.CharField(max_length=10, choices=Users.choices)

    def __str__(self):
        return self.consultant_name

class Order(models.Model):
    order_num           = models.CharField(max_length=100,unique=True)
    class Orders(models.TextChoices):
        NETWORK = 'تنفيذ شبكة'
        COUNTER = 'عداد'
        EMERGENCY = 'طوارئ'
        SUBSTITUTE = 'إحلال'
        REINFORCEMENT = 'التعزيز'
        EFFORT = 'الجهد المتوسط'
        PROJECTS = 'مشروع'
    order_type          = models.CharField(max_length=50, choices=Orders.choices)
    employment_type     = models.CharField(max_length=40,null=True,blank=True)
    contractor_name     = models.CharField(max_length=50)
    distract            = models.CharField(max_length=50)
    materials           = models.CharField(max_length=100,null=True,blank=True)
    date                = models.DateTimeField(auto_now_add=True)
    user                = models.ForeignKey(UserTable, on_delete=models.CASCADE)
    year                = models.CharField(max_length=5)
    month               = models.CharField(max_length=5)
    day                 = models.CharField(max_length=5)
    safety_violations   = models.BooleanField(default=False)
    archived            = models.BooleanField(default=False)

    def __str__(self):
        return str(self.order_num) + " " + self.order_type


def create_image(size, bgColor, message, font, fontColor):
    W, H = size
    image = Image.new('RGB', size, bgColor)
    draw = ImageDraw.Draw(image)
    _, _, w, h = draw.textbbox((0, 0), message, font=font)
    draw.text(((W-w)-20, (H-h)-110), message, font=font, fill=fontColor)
    return image

def create_image2(size, bgColor, message, font, fontColor,parent):
    W, H = size
    draw = ImageDraw.Draw(parent)
    _, _, w, h = draw.textbbox((0, 0), message, font=font)
    draw.text(((W-w)-20, (H-h)-20), message, font=font, fill=fontColor)

def create_image3(size, bgColor, message, font, fontColor,parent):
    W, H = size
    draw = ImageDraw.Draw(parent)
    _, _, w, h = draw.textbbox((0, 0), message, font=font)
    draw.text(((W-w)-20, (H-h)-50), message, font=font, fill=fontColor)

def create_image4(size, bgColor, message, font, fontColor,parent):
    W, H = size
    draw = ImageDraw.Draw(parent)
    _, _, w, h = draw.textbbox((0, 0), message, font=font)
    draw.text(((W-w)-20, (H-h)-80), message, font=font, fill=fontColor)



class Object(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    object_img = models.ImageField(default='img/unknown.png' , upload_to="object")

    # def updateImage(self, *args, **kwargs):
    #     reshaped_text = arabic_reshaper.reshape(self.order.user.consultant_name)
    #     bidi_text = bidi.algorithm.get_display(reshaped_text)
    #     reshaped_text2 = arabic_reshaper.reshape(self.order.distract)
    #     bidi_text2 = bidi.algorithm.get_display(reshaped_text2)
    #     reshaped_text3 = arabic_reshaper.reshape(str(self.order.date))
    #     bidi_text3 = bidi.algorithm.get_display(reshaped_text3)
    #     reshaped_text4 = arabic_reshaper.reshape("النماذج")
    #     bidi_text4 = bidi.algorithm.get_display(reshaped_text4)
    #     apath = self.object_img.path
    #     limg = Image.open(apath)
    #     isImageTakedWithPhone = is_taken_with_phone(apath)
    #     if isImageTakedWithPhone:
    #         limg = limg.rotate(-90, expand=True)
    #     limg = limg.resize((400,650))
    #     try:limg2 = Image.open(thePath)
    #     except:limg2 = Image.open('./static/img/logo.png')
    #     limg2.thumbnail((300,200))

    #     myFont = ImageFont.truetype(thePath, 35)
    #     myFont2 = ImageFont.truetype(thePath, 17)
    #     myMessage = bidi_text
    #     myMessage2 = bidi_text2
    #     myMessage3 = bidi_text3
    #     myMessage4 = bidi_text4
    #     myImage = create_image((400, 800), 'white', myMessage, myFont, 'black')
    #     text = create_image2((400, 800), 'white', myMessage2, myFont2, 'black',myImage)
    #     text3 = create_image3((400, 800), 'white', myMessage3, myFont2, 'black',myImage)
    #     text4 = create_image4((400, 800), 'white', myMessage4, myFont2, 'black',myImage)
    #     myImage.paste(limg,(0,0))
    #     myImage.paste(limg2,(0,0))

    #     myImage.save(apath)

    def updateImage(self, *args, **kwargs):
        super(Object, self).save(*args, **kwargs)

        reshaped_text = arabic_reshaper.reshape(self.order.user.consultant_name)
        bidi_text = bidi.algorithm.get_display(reshaped_text)
        reshaped_text2 = arabic_reshaper.reshape(self.order.distract)
        bidi_text2 = bidi.algorithm.get_display(reshaped_text2)
        reshaped_text3 = arabic_reshaper.reshape(str(self.order.date.date()))
        bidi_text3 = bidi.algorithm.get_display(reshaped_text3)
        reshaped_text4 = arabic_reshaper.reshape("النماذج")
        bidi_text4 = bidi.algorithm.get_display(reshaped_text4)
        apath = self.object_img.path
        limg = Image.open(apath)
        isImageTakedWithPhone = is_taken_with_phone(apath)
        if isImageTakedWithPhone:
            limg = limg.rotate(-90, expand=True)
        limg = limg.resize((400,650))
        try:limg2 = Image.open(theLogo)
        except:limg2 = Image.open('/home/assays/mzengineering/mz/static/img/logo.png')
        limg2.thumbnail((300,200))
        try:limg3 = Image.open(theLogo.replace("logo.png", "seal.jpg"))
        except:limg3 = Image.open('/home/assays/mzengineering/mz/static/img/seal.jpg')
        limg3.thumbnail((170,170))

        myFont = ImageFont.truetype(thePath, 35)
        myFont2 = ImageFont.truetype(thePath, 17)
        myMessage = bidi_text
        myMessage2 = bidi_text2
        myMessage3 = bidi_text3
        myMessage4 = bidi_text4
        myImage = create_image((400, 820), 'white', myMessage, myFont, 'black')
        text = create_image2((400, 820), 'white', myMessage2, myFont2, 'black',myImage)
        text3 = create_image3((400, 820), 'white', myMessage3, myFont2, 'black',myImage)
        text4 = create_image4((400, 820), 'white', myMessage4, myFont2, 'black',myImage)
        myImage.paste(limg,(0,0))
        myImage.paste(limg2,(0,0))
        myImage.paste(limg3,(0,720))

        myImage.save(apath)


class Address(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    address_img = models.ImageField(default='img/unknown.png' , upload_to="address")

    def updateImage(self, *args, **kwargs):
        reshaped_text = arabic_reshaper.reshape(self.order.user.consultant_name)
        bidi_text = bidi.algorithm.get_display(reshaped_text)
        reshaped_text2 = arabic_reshaper.reshape(self.order.distract)
        bidi_text2 = bidi.algorithm.get_display(reshaped_text2)
        reshaped_text3 = arabic_reshaper.reshape(str(self.order.date))
        bidi_text3 = bidi.algorithm.get_display(reshaped_text3)
        reshaped_text4 = arabic_reshaper.reshape("صور الموقع")
        bidi_text4 = bidi.algorithm.get_display(reshaped_text4)
        apath = self.address_img.path
        limg = Image.open(apath)
        isImageTakedWithPhone = is_taken_with_phone(apath)
        if isImageTakedWithPhone:
            limg = limg.rotate(-90, expand=True)
        limg = limg.resize((400,650))
        try:limg2 = Image.open(theLogo)
        except:limg2 = Image.open('/home/assays/mzengineering/mz/static/img/logo.png')
        limg2.thumbnail((300,200))

        myFont = ImageFont.truetype(thePath, 35)
        myFont2 = ImageFont.truetype(thePath, 17)
        myMessage = bidi_text
        myMessage2 = bidi_text2
        myMessage3 = bidi_text3
        myMessage4 = bidi_text4
        myImage = create_image((400, 800), 'white', myMessage, myFont, 'black')
        text = create_image2((400, 800), 'white', myMessage2, myFont2, 'black',myImage)
        text3 = create_image3((400, 800), 'white', myMessage3, myFont2, 'black',myImage)
        text4 = create_image4((400, 800), 'white', myMessage4, myFont2, 'black',myImage)
        myImage.paste(limg,(0,0))
        myImage.paste(limg2,(0,0))

        myImage.save(apath)


class Violation(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    violation_img = models.ImageField(default='img/unknown.png' , upload_to="violation_img")
    notes = models.TextField()