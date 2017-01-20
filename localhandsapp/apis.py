from django.http import JsonResponse

from localhandsapp.models import Scooper, Task
from localhandsapp.serializers import ScooperSerializer, TasksSerializer

def customer_get_scoopers(request):
    scoopers = ScooperSerializer(
        Scooper.objects.all().order_by("-id"),
        many = True,
        context = {"request": request}
    ).data

    return JsonResponse({"scoopers": scoopers})

def customer_get_tasks(request, scooper_id):
    tasks = TasksSerializer(
        Task.objects.filter(scooper_id=scooper_id).order_by("-id"),
        many=True
    ).data

    return JsonResponse({"tasks": tasks})

def customer_add_order(request):
    return JsonResponse({})

def customer_get_latest_order(request):
    return JsonResponse({})
