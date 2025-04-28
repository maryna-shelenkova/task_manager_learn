from django.urls import path
from . import views

urlpatterns = [
    path('tasks/', views.tasks_by_weekday, name='tasks-by-weekday'),
    path('subtasks/', views.subtasks_list, name='subtasks-list'),
    path('subtasks/filter/', views.subtasks_by_task_and_status, name='subtasks-filter'),
]
