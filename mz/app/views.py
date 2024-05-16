from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse, Http404
from .models import *
from datetime import *
from django.contrib.auth import logout as logout_auth
from django.contrib.auth import authenticate
from django.contrib import auth
from django.contrib.auth.models import User
from PIL import Image
import uuid
import os
from datetime import *

# Create your views here.
def login(request):
    context = {'lang':"ar"}
    if request.user.is_authenticated:
        return redirect("/")
    if request.method == "POST":
        ierr = ""
        errtitle = ""
        a = "work"
        nextUrl = ""
        jobNumFilter = UserTable.objects.filter(job_number=request.POST['jobNum'])
        if len(jobNumFilter) == 0:
            a = "no"
            ierr = "snack"
            errtitle = "الرقم الوظيفي غير صحيح"
        else:
            jobNumGet = UserTable.objects.get(job_number=request.POST['jobNum'])
        if a == "work":
            user = User.objects.get(pk = jobNumGet.main_user.pk)
            user = authenticate(username = user.username,password = request.POST["password"])
            if user is None:
                a = "no"
                ierr = "snack"
                errtitle = "كلمة المرور غير صحيحة"
        if a == "work":
            nextUrl = "/"
            auth.login(request,user)
        return JsonResponse({'ierr':ierr,'errtitle':errtitle,'nextUrl':nextUrl})
    return render(request, 'login.html', context)

def validateImageName(name):
    nums = "1234567890"
    for n in nums:
        name = name.replace(n,"")
    return name

def logout(request):
    logout_auth(request)
    return redirect("/")

def subscribers(request):
    context = {'lang':"ar"}
    if not request.user.is_authenticated:
        return redirect("/login")
    else:
        user = User.objects.get(pk=request.user.pk)
        userTable = UserTable.objects.get(main_user=user)
        context['user'] = userTable
    if request.method == "POST":
        errtitle = ""

        orderNumFilter = Order.objects.filter(order_num=request.POST["orderNum"])
        if orderNumFilter:
            errtitle = "رقم الطلب موجود مسبقاً!"
        if errtitle == "":
            violationCondition = False
            if request.POST["violationCondition"] == "on":
                violationCondition = True
            now = datetime.now()
            orderCreate = Order.objects.create(
                order_num = request.POST["orderNum"],
                order_type = request.POST["orderType"],
                contractor_name = request.POST["contractor"],
                distract = request.POST["distract"],
                user = userTable,
                year = now.year,
                month = now.month,
                day = now.day,
                safety_violations = violationCondition,
                archived = False
            )
            orderCreate.save()
            for file in request.FILES:
                fileType = file[:len(file)-1]
                if fileType == "objectBox":
                    objectImageCreate = Object.objects.create(
                        order = orderCreate,
                        object_img = request.FILES[file]
                    )
                    objectImageCreate.save()
                    objectImageCreate.updateImage()
                elif fileType == "addressBox":
                    addressImageCreate = Address.objects.create(
                        order = orderCreate,
                        address_img = request.FILES[file]
                    )
                    addressImageCreate.save()
                    addressImageCreate.updateImage()
                elif fileType == "violationsBox":
                    violationImageCreate = Violation.objects.create(
                        order = orderCreate,
                        violation_img = request.FILES[file]
                    )
                    violationImageCreate.save()
                    violationImageCreate.updateImage()
    else:
        data = []
        context['data']=data

    return render(request, 'subscribers.html', context)

def home(request):
    context = {'lang':"ar"}
    if not request.user.is_authenticated:
        return redirect("/login")
    else:
        user = User.objects.get(pk=request.user.pk)
        userTable = UserTable.objects.get(main_user=user)
        context['user'] = userTable
    if request.method == "POST":
        pass
    else:
        data = []
        context['data']=data

    return render(request, 'home.html', context)

def export(request, fileName):
    if request.user.is_authenticated:
        try:
            file_path = './media/exportPDF/'+fileName
            with open(file_path, 'rb') as fh:
                response = HttpResponse(fh.read(), content_type='application/pdf')
                response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file_path)
                return response
        except:
            file_path = '/home/assays/electricPortalWeb/electric_portal/media/exportPDF/'+fileName
            with open(file_path, 'rb') as fh:
                response = HttpResponse(fh.read(), content_type='application/pdf')
                response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file_path)
                return response
    raise Http404