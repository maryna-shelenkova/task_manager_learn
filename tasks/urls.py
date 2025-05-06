from django.urls import path
from . import views
from .views import CategoryListCreate, CategoryDetail



urlpatterns = [
    path('tasks/', views.TaskListCreateAPIView.as_view(), name='task-list-create'),
    path('tasks/<int:pk>/', views.TaskRetrieveUpdateDestroyAPIView.as_view(), name='task-detail'),
    path('subtasks/', views.SubTaskListCreateAPIView.as_view(), name='subtask-list-create'),
    path('subtasks/<int:pk>/', views.SubTaskRetrieveUpdateDestroyAPIView.as_view(), name='subtask-detail'),
    path('tasks/statistics/', views.TaskStatisticsAPIView.as_view(), name='task-statistics'),
    path('categories/', CategoryListCreate.as_view(), name='category-list-create'),
    path('categories/<int:pk>/', CategoryDetail.as_view(), name='category-detail'),
]


