# Create your views here.

from rest_framework_simplejwt.tokens import RefreshToken
from django.views.decorators.csrf import csrf_exempt
import json

from rest_framework.views import APIView
from rest_framework.response import Response

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.db.models import Q

from app.models import *

class home(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            data = []
            months = [1,2,3,4,5,6,7,8,9,10,11,12]
            for m in months:
                dataFilter = Order.objects.filter(month=str(m),archived=True)
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
                    if request.GET['category'] in ("subscribers", "operations", "projects", "readyFiles"):
                        order_types = {
                            "subscribers": ("عداد", "تنفيذ شبكة"),
                            "operations": ("طوارئ", "إحلال", "التعزيز", "الجهد المتوسط"),
                            "projects": (""),
                            "readyFiles": (""),
                        }
                        if d.order_type in order_types[request.GET['category']]:
                            now = datetime(int(d.year), int(d.month), int(d.day))
                            dayName = {
                                'Sunday': "الأحد",
                                'Monday': "الإثنين",
                                'Tuesday': "الثلاثاء",
                                'Wednesday': "الأربعاء",
                                'Thursday': "الخميس",
                                'Friday': "الجمعة",
                                'Saturday': "السبت"
                            }[now.strftime('%A')]
                            values.append([d.order_num, d.order_type, f'{d.day} {dayName}', d.pk])

                if len(values) != 0:
                    values = values[::-1]
                    data.append([monthName,values])
            data = data[::-1]
            return Response({'message': request.GET['category']}, status=200)
        else:
            return Response({'message': "Unauthorized access"}, status=401)

@csrf_exempt
def login(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            jobNum = data.get('jobNum')
            password = data.get('password')

            jobNumFilter = UserTable.objects.filter(job_number=jobNum)
            if len(jobNumFilter) == 0:
                a = "no"
                errtitle = "الرقم الوظيفي غير صحيح"
            else:
                jobNumGet = UserTable.objects.get(job_number=jobNum)
            if a == "work":
                user = User.objects.get(pk = jobNumGet.main_user.pk)
                user = authenticate(username = user.username,password = password)
                if user is None:
                    a = "no"
                    errtitle = "كلمة المرور غير صحيحة"
            if a == "work":
                auth.login(request,user)
            return JsonResponse({"errtitle":errtitle})
        except json.JSONDecodeError:
            return JsonResponse({'message': 'Invalid JSON'}, status=400)
    return JsonResponse({'message': 'Invalid request method'}, status=405)