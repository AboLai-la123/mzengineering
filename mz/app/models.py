from django.db import models
from django.contrib.auth.models import User
from PIL import Image, ImageDraw, ImageFont

import arabic_reshaper
import bidi.algorithm
import os
from bidi.algorithm import get_display

if os.path.expanduser("~") == 'C:\\Users\\H1720':
    thePath = r"C:\Users\H1720\Documents\mz-engineering\mz\static\fonts\arial.ttf"
    theLogo = r"C:\Users\H1720\Documents\mz-engineering\mz\static\img\logo.png"
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
        READYFILES = 'ملفات جاهزة'
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
    pdf_file_name       = models.TextField(null=True,blank=True)

    def __str__(self):
        return str(self.order_num) + " " + self.order_type

def resize_image(image, base_width):
    width_percent = (base_width / float(image.size[0]))
    height_size = int((float(image.size[1]) * float(width_percent)))
    return image.resize((base_width, height_size), Image.LANCZOS)

def is_arabic(text):
    for character in text:
        if '\u0600' <= character <= '\u06FF' or '\u0750' <= character <= '\u077F' or '\u08A0' <= character <= '\u08FF' or '\uFB50' <= character <= '\uFDFF' or '\uFE70' <= character <= '\uFEFF':
            return True
    return False

def add_logo(image, logo_path):
    with Image.open(logo_path) as logo:
        logo.thumbnail((100, 100), Image.LANCZOS)  # قم بتعديل الحجم حسب الحاجة
        image.paste(logo, (10, 10), logo.convert("RGBA"))
    return image

class Object(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    object_img = models.ImageField(default='img/unknown.png', upload_to="object")

    def delete(self, using=None, keep_parents=False):
        self.object_img.delete()
        super().delete()

class Address(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    address_img = models.ImageField(default='img/unknown.png', upload_to="address")

    def delete(self, using=None, keep_parents=False):
        self.address_img.delete()
        super().delete()

    def updateImage(self, *args, **kwargs):
        texts = [self.order.user.consultant_name, self.order.distract, str(self.order.date), "صور الموقع"]
        base_width = 700
        logo_path = "/home/assays/mzengineering/mz/static/img/logo.png"

        with Image.open(self.address_img.path) as original_image:
            if original_image.width != base_width:
                resized_image = resize_image(original_image, base_width)
                resized_image.save(self.address_img.path)

        with Image.open(self.address_img.path) as image:
            image = add_logo(image, logo_path)
            draw = ImageDraw.Draw(image)
            font_path = "/home/assays/mzengineering/mz/static/fonts/arial.ttf"
            font_size = 36
            font = ImageFont.truetype(font_path, font_size)

            width, height = image.size
            padding = 10
            vertical_spacing = 10
            initial_y = height - padding

            for text in texts[::-1]:
                if is_arabic(text):
                    reshaped_text = arabic_reshaper.reshape(text)
                    bidi_text = get_display(reshaped_text[::-1])
                else:
                    bidi_text = text

                text_width, text_height = draw.textbbox((0, 0), bidi_text, font=font)[2:4]
                x = width - text_width - padding
                y = initial_y - text_height

                shadow_offset = 2
                draw.text((x + shadow_offset, y + shadow_offset), bidi_text, font=font, fill="black")
                draw.text((x, y), bidi_text, font=font, fill="white")

                initial_y = y - vertical_spacing

            image.save(self.address_img.path)


class Violation(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    violation_img = models.ImageField(default='img/unknown.png' , upload_to="violation_img")
    notes = models.TextField()

    def delete(self, using=None, keep_parents=False):
        self.violation_img.delete()
        super().delete()

    def updateImage(self, *args, **kwargs):
        texts = [self.order.user.consultant_name, self.order.distract, str(self.order.date), "المخالفات"]
        base_width = 700
        logo_path = "/home/assays/mzengineering/mz/static/img/logo.png"

        with Image.open(self.violation_img.path) as original_image:
            if original_image.width != base_width:
                resized_image = resize_image(original_image, base_width)
                resized_image.save(self.violation_img.path)

        with Image.open(self.violation_img.path) as image:
            image = add_logo(image, logo_path)
            draw = ImageDraw.Draw(image)
            font_path = "/home/assays/mzengineering/mz/static/fonts/arial.ttf"
            font_size = 36
            font = ImageFont.truetype(font_path, font_size)

            width, height = image.size
            padding = 10
            vertical_spacing = 10
            initial_y = height - padding

            for text in texts[::-1]:
                if is_arabic(text):
                    reshaped_text = arabic_reshaper.reshape(text)
                    bidi_text = get_display(reshaped_text[::-1])
                else:
                    bidi_text = text

                text_width, text_height = draw.textbbox((0, 0), bidi_text, font=font)[2:4]
                x = width - text_width - padding
                y = initial_y - text_height

                shadow_offset = 2
                draw.text((x + shadow_offset, y + shadow_offset), bidi_text, font=font, fill="black")
                draw.text((x, y), bidi_text, font=font, fill="white")

                initial_y = y - vertical_spacing

            image.save(self.violation_img.path)



# from PIL import Image, ImageDraw, ImageFont
# import arabic_reshaper
# from django.db import models
# from django.contrib.auth.models import User


# class UserTable(models.Model):
#     main_user       = models.ForeignKey(User,on_delete=models.CASCADE)
#     consultant_name = models.CharField(max_length=50)
#     job_number      = models.CharField(max_length=50)
#     phone           = models.CharField(max_length=13)
#     class Users(models.TextChoices):
#         ADMIN = "admin"
#         USER  = "user"
#     user_role       = models.CharField(max_length=10, choices=Users.choices)

#     def __str__(self):
#         return self.consultant_name

# class Order(models.Model):
#     order_num           = models.CharField(max_length=100,unique=True)
#     class Orders(models.TextChoices):
#         NETWORK = 'تنفيذ شبكة'
#         COUNTER = 'عداد'
#         EMERGENCY = 'طوارئ'
#         SUBSTITUTE = 'إحلال'
#         REINFORCEMENT = 'التعزيز'
#         EFFORT = 'الجهد المتوسط'
#         PROJECTS = 'مشروع'
#         READYFILES = 'ملفات جاهزة'
#     order_type          = models.CharField(max_length=50, choices=Orders.choices)
#     employment_type     = models.CharField(max_length=40,null=True,blank=True)
#     contractor_name     = models.CharField(max_length=50)
#     distract            = models.CharField(max_length=50)
#     materials           = models.CharField(max_length=100,null=True,blank=True)
#     date                = models.DateTimeField(auto_now_add=True)
#     user                = models.ForeignKey(UserTable, on_delete=models.CASCADE)
#     year                = models.CharField(max_length=5)
#     month               = models.CharField(max_length=5)
#     day                 = models.CharField(max_length=5)
#     safety_violations   = models.BooleanField(default=False)
#     archived            = models.BooleanField(default=False)
#     pdf_file_name       = models.TextField(null=True,blank=True)

#     def __str__(self):
#         return str(self.order_num) + " " + self.order_type





# class Violation(models.Model):
#     order = models.ForeignKey(Order, on_delete=models.CASCADE)
#     violation_img = models.ImageField(default='img/unknown.png' , upload_to="violation_img")
#     notes = models.TextField()

#     def delete(self, using=None, keep_parents=False):
#         self.violation_img.delete()
#         super().delete()