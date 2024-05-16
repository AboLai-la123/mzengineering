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

def operations(request):
    context = {'lang':"ar"}
    if not request.user.is_authenticated:
        return redirect("/login")
    else:
        user = User.objects.get(pk=request.user.pk)
        userTable = UserTable.objects.get(main_user=user)
        context['user'] = userTable
    if request.method == "POST":
        errtitle = ""
        nextUrl = ""
        if "orderPK" in request.POST:
            'violationBoxE4', 'note4', 'noteE2'
            'objectBoxE1', 'addressBoxE1', 'violationsBoxE2'
            orderFilter = Order.objects.filter(pk = request.POST["orderPK"])
            if len(orderFilter) == 0:
                errtitle = "الطلب المراد تعديله غير موجود او تم حذفة"
            else:
                orderGet = Order.objects.get(pk = int(request.POST["orderPK"]))
            if errtitle == "":
                violationCondition = False
                if request.POST["violationConditionE"] == "yes":
                    violationCondition = True
                isArchive = False
                if request.POST["isArchiveE"] == "yes":
                    isArchive = True
                orderGet.order_num = request.POST["orderNumE"]
                orderGet.order_type = request.POST["orderTypeE"]
                orderGet.contractor_name = request.POST["contractorE"]
                orderGet.distract = request.POST["distractE"]
                orderGet.safety_violations = violationCondition
                orderGet.archived = isArchive
                orderGet.save()
                postImages = []
                for image in request.POST:
                    if "violationBoxE" in image:
                        postImages.append(image.replace("violationBoxE",""))
                    if "objectBoxE" in image:
                        postImages.append(image.replace("objectBoxE",""))
                    if "addressBoxE" in image:
                        postImages.append(image.replace("addressBoxE",""))
                objectsFilter = Object.objects.filter(order = orderGet)
                for objectFile in objectsFilter:
                    if objectFile.pk not in postImages:
                        objectFile.object_img.delete()
                        objectFile.delete()
                addressesFilter = Address.objects.filter(order = orderGet)
                for addressFile in addressesFilter:
                    if addressFile.pk not in postImages:
                        addressFile.address_img.delete()
                        addressFile.delete()
                violationsFilter = Violation.objects.filter(order = orderGet)
                for violationFile in violationsFilter:
                    if violationFile.pk not in postImages:
                        violationFile.violation_img.delete()
                        violationFile.delete()
                for file in request.FILES:
                    if "objectBox" in file:
                        objectImageCreate = Object.objects.create(
                            order = orderGet,
                            object_img = request.FILES[file]
                        )
                        objectImageCreate.save()
                        objectImageCreate.updateImage()
                    elif "addressBox" in file:
                        addressImageCreate = Address.objects.create(
                            order = orderGet,
                            address_img = request.FILES[file]
                        )
                        addressImageCreate.save()
                        addressImageCreate.updateImage()
                    elif "violationsBox" in file:
                        violationImageCreate = Violation.objects.create(
                            order = orderGet,
                            violation_img = request.FILES[file],
                            notes = request.POST[f"note{file.replace('violationsBox','')}"]
                        )
                        violationImageCreate.save()
        else:

            orderNumFilter = Order.objects.filter(order_num=request.POST["orderNum"])
            if orderNumFilter:
                errtitle = "رقم الطلب موجود مسبقاً!"
            if errtitle == "":
                violationCondition = False
                if request.POST["violationCondition"] == "on":
                    violationCondition = True
                now = datetime.now()
                archived = False
                if request.POST["isArchive"] == "yes":
                    archived = True
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
                    archived = archived
                )
                orderCreate.save()
                for file in request.FILES:
                    if "objectBox" in file:
                        objectImageCreate = Object.objects.create(
                            order = orderCreate,
                            object_img = request.FILES[file]
                        )
                        objectImageCreate.save()
                        objectImageCreate.updateImage()
                    elif "addressBox" in file:
                        addressImageCreate = Address.objects.create(
                            order = orderCreate,
                            address_img = request.FILES[file]
                        )
                        addressImageCreate.save()
                        addressImageCreate.updateImage()
                    elif "violationsBox" in file:
                        violationImageCreate = Violation.objects.create(
                            order = orderCreate,
                            violation_img = request.FILES[file],
                            notes = request.POST[f"note{file.replace('violationsBox','')}"]
                        )
                        violationImageCreate.save()
                nextUrl = "/"
        return JsonResponse({"errtitle":errtitle, "nextUrl":nextUrl})
    else:
        data = []
        months = [1,2,3,4,5,6,7,8,9,10,11,12]
        for m in months:
            dataFilter = Order.objects.filter(month=str(m),archived=True,)
            if m == 1:monthName = "يناير"
            if m == 2:monthName = "فبراير"
            if m == 3:monthName = "مارس"
            if m == 4:monthName = "إبريل"
            if m == 5:monthName = "مايو"
            if m == 6:monthName = "يونيو"
            if m == 7:monthName = "يوليو"
            if m == 8:monthName = "أغسطس"
            if m == 9:monthName = "سبتمبر"
            if m == 10:monthName = "أكتوبر"
            if m == 11:monthName = "نوفمبر"
            if m == 12:monthName = "ديسمبر"
            values = []
            for d in dataFilter:
                if d.order_type == "تنفيذ شبكة" or d.order_type == "عداد":
                    now = datetime(int(d.year),int(d.month),int(d.day))
                    if now.strftime('%A') == 'Sunday':dayName = "الأحد"
                    if now.strftime('%A') == 'Monday':dayName = "الإثنين"
                    if now.strftime('%A') == 'Tuesday':dayName = "الثلاثاء"
                    if now.strftime('%A') == 'Wednesday':dayName = "الأربعاء"
                    if now.strftime('%A') == 'Thursday':dayName = "الخميس"
                    if now.strftime('%A') == 'Friday':dayName = "الجمعة"
                    if now.strftime('%A') == 'Saturday':dayName = "السبت"
                    values.append([d.order_num,d.order_type,f'{d.day} {dayName}',d.pk])
            if len(values) != 0:
                values = values[::-1]
                data.append([monthName,values])
        data = data[::-1]
        if "getData" in request.GET:
            return JsonResponse({"data":data})
        elif "getOrder" in request.GET:
            order = Order.objects.get(pk = int(request.GET["pk"]))
            data = [
                order.pk,
                order.order_num,
                order.order_type,
                order.contractor_name,
                order.distract,
                order.safety_violations,
            ]
            objects = []
            imageFilter = Object.objects.filter(order=order)
            for image in imageFilter:
                imagePathLength = image.object_img.url.split("/")
                objects.append([image.object_img.url,image.pk,imagePathLength[len(imagePathLength)-1]])
            addresses = []
            imageFilter = Address.objects.filter(order=order)
            for image in imageFilter:
                imagePathLength = image.address_img.url.split("/")
                addresses.append([image.address_img.url,image.pk,imagePathLength[len(imagePathLength)-1]])
            violations = []
            imageFilter = Violation.objects.filter(order=order)
            for image in imageFilter:
                imagePathLength = image.violation_img.url.split("/")
                violations.append([image.violation_img.url,image.pk,imagePathLength[len(imagePathLength)-1],image.notes])
            return JsonResponse({
                "data": data,
                "objects": objects,
                "addresses": addresses,
                "violations": violations,
            })
        elif "search" in request.GET:
            data = []
            assayFilter = Assay.objects.filter(assay_num__icontains=request.GET["search"])
            for a in assayFilter:
                now = datetime(int(a.year),int(a.month),int(a.day))
                if now.strftime('%A') == 'Sunday':dayName = "الأحد"
                if now.strftime('%A') == 'Monday':dayName = "الإثنين"
                if now.strftime('%A') == 'Tuesday':dayName = "الثلاثاء"
                if now.strftime('%A') == 'Wednesday':dayName = "الأربعاء"
                if now.strftime('%A') == 'Thursday':dayName = "الخميس"
                if now.strftime('%A') == 'Friday':dayName = "الجمعة"
                if now.strftime('%A') == 'Saturday':dayName = "السبت"
                data.append([a.assay_num,a.user.consultant_name,f'{a.day} {dayName}'])
            return JsonResponse({"data":data})
        context['data']=data

    return render(request, 'operations.html', context)

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
        nextUrl = ""
        if "orderPK" in request.POST:
            'violationBoxE4', 'note4', 'noteE2'
            'objectBoxE1', 'addressBoxE1', 'violationsBoxE2'
            orderFilter = Order.objects.filter(pk = request.POST["orderPK"])
            if len(orderFilter) == 0:
                errtitle = "الطلب المراد تعديله غير موجود او تم حذفة"
            else:
                orderGet = Order.objects.get(pk = int(request.POST["orderPK"]))
            if errtitle == "":
                violationCondition = False
                if request.POST["violationConditionE"] == "yes":
                    violationCondition = True
                isArchive = False
                if request.POST["isArchiveE"] == "yes":
                    isArchive = True
                orderGet.order_num = request.POST["orderNumE"]
                orderGet.order_type = request.POST["orderTypeE"]
                orderGet.contractor_name = request.POST["contractorE"]
                orderGet.distract = request.POST["distractE"]
                orderGet.safety_violations = violationCondition
                orderGet.archived = isArchive
                orderGet.save()
                postImages = []
                for image in request.POST:
                    if "violationBoxE" in image:
                        postImages.append(image.replace("violationBoxE",""))
                    if "objectBoxE" in image:
                        postImages.append(image.replace("objectBoxE",""))
                    if "addressBoxE" in image:
                        postImages.append(image.replace("addressBoxE",""))
                objectsFilter = Object.objects.filter(order = orderGet)
                for objectFile in objectsFilter:
                    if objectFile.pk not in postImages:
                        objectFile.object_img.delete()
                        objectFile.delete()
                addressesFilter = Address.objects.filter(order = orderGet)
                for addressFile in addressesFilter:
                    if addressFile.pk not in postImages:
                        addressFile.address_img.delete()
                        addressFile.delete()
                violationsFilter = Violation.objects.filter(order = orderGet)
                for violationFile in violationsFilter:
                    if violationFile.pk not in postImages:
                        violationFile.violation_img.delete()
                        violationFile.delete()
                for file in request.FILES:
                    if "objectBox" in file:
                        objectImageCreate = Object.objects.create(
                            order = orderGet,
                            object_img = request.FILES[file]
                        )
                        objectImageCreate.save()
                        objectImageCreate.updateImage()
                    elif "addressBox" in file:
                        addressImageCreate = Address.objects.create(
                            order = orderGet,
                            address_img = request.FILES[file]
                        )
                        addressImageCreate.save()
                        addressImageCreate.updateImage()
                    elif "violationsBox" in file:
                        violationImageCreate = Violation.objects.create(
                            order = orderGet,
                            violation_img = request.FILES[file],
                            notes = request.POST[f"note{file.replace('violationsBox','')}"]
                        )
                        violationImageCreate.save()
        else:

            orderNumFilter = Order.objects.filter(order_num=request.POST["orderNum"])
            if orderNumFilter:
                errtitle = "رقم الطلب موجود مسبقاً!"
            if errtitle == "":
                violationCondition = False
                if request.POST["violationCondition"] == "on":
                    violationCondition = True
                now = datetime.now()
                archived = False
                if request.POST["isArchive"] == "yes":
                    archived = True
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
                    archived = archived
                )
                orderCreate.save()
                for file in request.FILES:
                    if "objectBox" in file:
                        objectImageCreate = Object.objects.create(
                            order = orderCreate,
                            object_img = request.FILES[file]
                        )
                        objectImageCreate.save()
                        objectImageCreate.updateImage()
                    elif "addressBox" in file:
                        addressImageCreate = Address.objects.create(
                            order = orderCreate,
                            address_img = request.FILES[file]
                        )
                        addressImageCreate.save()
                        addressImageCreate.updateImage()
                    elif "violationsBox" in file:
                        violationImageCreate = Violation.objects.create(
                            order = orderCreate,
                            violation_img = request.FILES[file],
                            notes = request.POST[f"note{file.replace('violationsBox','')}"]
                        )
                        violationImageCreate.save()
                nextUrl = "/"
        return JsonResponse({"errtitle":errtitle, "nextUrl":nextUrl})
    else:
        data = []
        months = [1,2,3,4,5,6,7,8,9,10,11,12]
        for m in months:
            dataFilter = Order.objects.filter(month=str(m),archived=True,)
            if m == 1:monthName = "يناير"
            if m == 2:monthName = "فبراير"
            if m == 3:monthName = "مارس"
            if m == 4:monthName = "إبريل"
            if m == 5:monthName = "مايو"
            if m == 6:monthName = "يونيو"
            if m == 7:monthName = "يوليو"
            if m == 8:monthName = "أغسطس"
            if m == 9:monthName = "سبتمبر"
            if m == 10:monthName = "أكتوبر"
            if m == 11:monthName = "نوفمبر"
            if m == 12:monthName = "ديسمبر"
            values = []
            for d in dataFilter:
                if d.order_type == "تنفيذ شبكة" or d.order_type == "عداد":
                    now = datetime(int(d.year),int(d.month),int(d.day))
                    if now.strftime('%A') == 'Sunday':dayName = "الأحد"
                    if now.strftime('%A') == 'Monday':dayName = "الإثنين"
                    if now.strftime('%A') == 'Tuesday':dayName = "الثلاثاء"
                    if now.strftime('%A') == 'Wednesday':dayName = "الأربعاء"
                    if now.strftime('%A') == 'Thursday':dayName = "الخميس"
                    if now.strftime('%A') == 'Friday':dayName = "الجمعة"
                    if now.strftime('%A') == 'Saturday':dayName = "السبت"
                    values.append([d.order_num,d.order_type,f'{d.day} {dayName}',d.pk])
            if len(values) != 0:
                values = values[::-1]
                data.append([monthName,values])
        data = data[::-1]
        if "getData" in request.GET:
            return JsonResponse({"data":data})
        elif "getOrder" in request.GET:
            order = Order.objects.get(pk = int(request.GET["pk"]))
            data = [
                order.pk,
                order.order_num,
                order.order_type,
                order.contractor_name,
                order.distract,
                order.safety_violations,
            ]
            objects = []
            imageFilter = Object.objects.filter(order=order)
            for image in imageFilter:
                imagePathLength = image.object_img.url.split("/")
                objects.append([image.object_img.url,image.pk,imagePathLength[len(imagePathLength)-1]])
            addresses = []
            imageFilter = Address.objects.filter(order=order)
            for image in imageFilter:
                imagePathLength = image.address_img.url.split("/")
                addresses.append([image.address_img.url,image.pk,imagePathLength[len(imagePathLength)-1]])
            violations = []
            imageFilter = Violation.objects.filter(order=order)
            for image in imageFilter:
                imagePathLength = image.violation_img.url.split("/")
                violations.append([image.violation_img.url,image.pk,imagePathLength[len(imagePathLength)-1],image.notes])
            return JsonResponse({
                "data": data,
                "objects": objects,
                "addresses": addresses,
                "violations": violations,
            })
        elif "search" in request.GET:
            data = []
            assayFilter = Assay.objects.filter(assay_num__icontains=request.GET["search"])
            for a in assayFilter:
                now = datetime(int(a.year),int(a.month),int(a.day))
                if now.strftime('%A') == 'Sunday':dayName = "الأحد"
                if now.strftime('%A') == 'Monday':dayName = "الإثنين"
                if now.strftime('%A') == 'Tuesday':dayName = "الثلاثاء"
                if now.strftime('%A') == 'Wednesday':dayName = "الأربعاء"
                if now.strftime('%A') == 'Thursday':dayName = "الخميس"
                if now.strftime('%A') == 'Friday':dayName = "الجمعة"
                if now.strftime('%A') == 'Saturday':dayName = "السبت"
                data.append([a.assay_num,a.user.consultant_name,f'{a.day} {dayName}'])
            return JsonResponse({"data":data})
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