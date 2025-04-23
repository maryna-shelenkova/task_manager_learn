from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils.timezone import now
from django.db.models import Count, Q

from .models import Task
from .serializers import TaskSerializer


# Задание 2 — Список всех задач
class TaskListView(generics.ListAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


# Задание 2 — Получение задачи по ID
class TaskDetailView(generics.RetrieveAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    lookup_field = 'id'


# Задание 3 — Агрегирующий эндпоинт
class TaskStatsView(APIView):
    def get(self, request):
        total_tasks = Task.objects.count()
        tasks_by_status = Task.objects.values('status').annotate(count=Count('id'))
        overdue_tasks = Task.objects.filter(deadline__lt=now(), status__in=["New", "In Progress", "Pending", "Blocked"]).count()

        return Response({
            'total_tasks': total_tasks,
            'tasks_by_status': {item['status']: item['count'] for item in tasks_by_status},
            'overdue_tasks': overdue_tasks,
        })

