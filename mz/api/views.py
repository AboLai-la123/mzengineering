# Create your views here.

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db.models import Q
from django.shortcuts import get_object_or_404
from datetime import *
import uuid

from app.models import *
from django.contrib.auth import authenticate
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from rest_framework import status
import re
from PIL import Image

from django.middleware.csrf import get_token

def csrfmiddlewaretoken(request):
    # استرجاع التوكن CSRF
    csrf_token = get_token(request)
    # إرجاع التوكن كاستجابة JSON
    return JsonResponse({'csrfToken': csrf_token})

@csrf_exempt
def checkData(request):
    if request.method == "POST":
        order_exists = Order.objects.filter(order_num=request.POST["requestNumber"]).exists()
        return JsonResponse({"exists": not order_exists}, status=200 if order_exists else 404)
    return JsonResponse({"message": "Invalid request method"}, status=405)

class getData(APIView):
    def get(self, request):
        if not request.user.is_authenticated:
            return Response({'message': "Unauthorized access"}, status=401)

        order_num = request.GET.get("orderNum")
        order = Order.objects.get(order_num=order_num)
        base_url = "http://assays.pythonanywhere.com"

        data = {
            "pk": order.pk,
            "requestNumber": order.order_num,
            "workType": order.order_type,
            "date": order.date,
            "contractor": order.contractor_name,
            "district": order.distract,
            "materials": order.materials,
            "safetyViolation": order.safety_violations,
            "images": {
                "object": [
                    [f"{base_url}{obj.object_img.url}", obj.pk]
                    for obj in Object.objects.filter(order=order)
                ],
                "location": [
                    [f"{base_url}{addr.address_img.url}", addr.pk]
                    for addr in Address.objects.filter(order=order)
                ],
                "violation": [
                    [f"{base_url}{violation.violation_img.url}", violation.notes, violation.pk]
                    for violation in Violation.objects.filter(order=order)
                ],
            },
        }
        return Response({'message': data}, status=200)

class home(APIView):
    def get_model_and_field(self, file_name):
        if "object_" in file_name:
            return Object, 'object_img'
        elif "location_" in file_name:
            return Address, 'address_img'
        elif "violation_" in file_name:
            return Violation, 'violation_img'
        return None, None

    def post(self, request):
        if request.user.is_authenticated:
            data = request.POST
            print(data)

            # التحقق من وجود requestNumber
            if 'requestNumber' not in data:
                return Response({'error': 'requestNumber is required'}, status=400)
            requestNumber = data['requestNumber']

            # التحقق من الصيغة الصحيحة للـ requestNumber
            if not requestNumber.isdigit():
                return Response({'error': 'requestNumber must contain only digits'}, status=400)

            # التحقق من طول الـ requestNumber
            if len(requestNumber) > 100:
                return Response({'error': 'requestNumber must be at most 100 characters'}, status=400)

            # التحقق من الـ order_num الفريد إذا كانت هناك عملية تحديث
            if 'pk' in data:
                order = Order.objects.get(pk=int(data['pk']))
                if order.order_num != requestNumber:
                    return Response({'error': 'requestNumber must be unique'}, status=400)
            else:
                if Order.objects.filter(order_num=requestNumber).exists():
                    return Response({'error': 'requestNumber must be unique'}, status=400)

            # التحقق من وجود contractor
            if 'contractor' not in data:
                return Response({'error': 'contractor is required'}, status=400)
            contractor = data['contractor']

            # التحقق من طول contractor
            if len(contractor) > 50:
                return Response({'error': 'contractor must be at most 50 characters'}, status=400)

            # التحقق من وجود district
            if 'district' not in data:
                return Response({'error': 'district is required'}, status=400)
            district = data['district']

            # التحقق من طول district
            if len(district) > 50:
                return Response({'error': 'district must be at most 50 characters'}, status=400)

            # التحقق من وجود workType وصحته
            if 'workType' not in data:
                return Response({'error': 'workType is required'}, status=400)
            workType = data['workType']
            valid_work_types = ['عداد', 'تنفيذ شبكة', 'طوارئ', 'إحلال', 'تعزيز', 'الجهد المتوسط', 'مشروع', 'ملفات جاهزة']
            if workType not in valid_work_types:
                return Response({'error': 'workType must be valid choice'}, status=400)

            # التحقق من وجود safetyViolation
            if 'safetyViolation' not in data:
                return Response({'error': 'violation is required'}, status=400)
            violationCondition = data['safetyViolation'] == "توجد"

            # التحقق من وجود archived
            if 'archived' not in data:
                return Response({'error': 'archived is required'}, status=400)
            archived = data['archived']
            if archived not in ['true', 'false']:
                return Response({'error': 'archived must be "true" or "false"'}, status=400)
            else:
                archived = archived == "true"

            # التحقق من الصور
            for key, value in request.FILES.items():
                if key.startswith('object_') or key.startswith('violation_') or key.startswith('location_'):
                    try:
                        # التحقق من الصور باستخدام PIL
                        Image.open(value)
                    except Exception as e:
                        return Response({'error': f'{key} must be an image'}, status=400)

            # حفظ البيانات في قاعدة البيانات

            model_field_mapping = {
                'deletedSelectedImages': ('object_img', Object),
                'deletedSelectedLocationImages': ('address_img', Address),
                'deletedSelectedSafetyViolationImages': ('violation_img', Violation),
            }

            if 'pk' in data:
                # عملية التحديث
                # ابدأ بتحديث البيانات الأساسية للطلب
                notes = {key.replace("updatedNote_", ""): value for key, value in request.POST.items() if key.startswith('updatedNote_')}
                for notePk, value in notes.items():
                    violationGet = Violation.objects.get(pk=notePk)
                    violationGet.notes = value
                    violationGet.save()

                for key, value in request.POST.items():
                    if key in model_field_mapping:
                        field, model = model_field_mapping.get(key)
                        if model:
                            if value.strip() != "":
                                for val in value.split(','):
                                    image = model.objects.get(pk=int(val))
                                    image_field = getattr(image, field)
                                    image_field.delete()
                                    image.delete()

                order.order_type = workType
                order.archived = archived
                order.safety_violations = violationCondition
                order.save()

                # حذف الصور القديمة ثم إضافة الجديدة
                # Object.objects.filter(order=order).delete()
                # Address.objects.filter(order=order).delete()
                # Violation.objects.filter(order=order).delete()
            else:
                # عملية الحفظ
                userTable = UserTable.objects.get(main_user=request.user)
                now = datetime.now()
                pdfFileName = f'{uuid.uuid4().hex}.pdf'
                order = Order.objects.create(
                    order_num=requestNumber,
                    order_type=workType,
                    contractor_name=contractor,
                    distract=district,
                    user=userTable,
                    year=now.year,
                    month=now.month,
                    day=now.day,
                    safety_violations=violationCondition,
                    archived=archived,
                    pdf_file_name=pdfFileName,
                    materials=request.POST.get("materials") if not None else ""
                )
                order.save()

            for file_name in request.FILES:
                model, img_field = self.get_model_and_field(file_name)
                if model:
                    image_instance = model.objects.create(order=order, **{img_field: request.FILES[file_name]})

                    if hasattr(image_instance, 'updateImage'):
                        image_instance.updateImage()

                    if "violation_" in file_name:
                        note_key = f"note_{file_name.replace('violation_', '')}"
                        image_instance.notes = request.POST.get(note_key, "")

                    image_instance.save()

            return Response({'success': 'Data validated successfully'}, status=200)
        else:
            return Response({'message': "Unauthorized access"}, status=401)


    def get(self, request):
        if request.user.is_authenticated:
            months = range(1, 13)
            month_names = [
                "يناير", "فبراير", "مارس", "إبريل", "مايو", "يونيو",
                "يوليو", "أغسطس", "سبتمبر", "أكتوبر", "نوفمبر", "ديسمبر"
            ]
            day_names = {
                'Sunday': "الأحد", 'Monday': "الإثنين", 'Tuesday': "الثلاثاء",
                'Wednesday': "الأربعاء", 'Thursday': "الخميس",
                'Friday': "الجمعة", 'Saturday': "السبت"
            }
            order_types = {
                "Subscribers": ("عداد", "تنفيذ شبكة"),
                "Operations": ("طوارئ", "إحلال", "التعزيز", "الجهد المتوسط"),
                "Projects": ("مشروع"),
                "ReadyFiles": ("ملفات جاهزة")
            }

            category = request.GET.get('category')
            archived = category is not None

            data = [
                {
                    "date": f'{day_names[datetime(int(d.year), int(d.month), int(d.day)).strftime("%A")]} {d.day}',
                    "id": d.order_num,
                    "month": month_names[m - 1],
                    "type": d.order_type
                }
                for m in months
                for d in Order.objects.filter(month=str(m), archived=archived)
                if not category or d.order_type in order_types.get(category, [])
            ]
            return Response({'message': data}, status=200)
        else:
            return Response({'message': "Unauthorized access"}, status=401)

def login(request):
    if request.method == 'POST':
        try:
            jobNum = request.POST.get('jobNum')
            password = request.POST.get('password')

            if not jobNum or not password:
                return JsonResponse({'message': 'البيانات المدخلة غير صحيحة'}, status=400)

            jobNumGet = get_object_or_404(UserTable, job_number=jobNum)
            user = authenticate(username=jobNumGet.main_user.username, password=password)

            if user is None:
                return JsonResponse({'message': 'كلمة المرور غير صحيحة'}, status=400)

            refresh = RefreshToken.for_user(user)
            return JsonResponse({'access': str(refresh.access_token)}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({'message': 'Invalid JSON'}, status=400)

    return JsonResponse({'message': 'Invalid request method'}, status=405)