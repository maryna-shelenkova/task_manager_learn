from django.urls import path
from .views import TaskListView, TaskDetailView, TaskStatsView

urlpatterns = [
    path('', TaskListView.as_view(), name='task-list'),
    path('<int:id>/', TaskDetailView.as_view(), name='task-detail'),
    path('stats/', TaskStatsView.as_view(), name='task-stats'),
]
