from django.urls import path
from .views import SubTaskListCreateView, SubTaskDetailUpdateDeleteView

urlpatterns = [
    path('subtasks/', SubTaskListCreateView.as_view(), name='subtask-list'),
    path('subtasks/<int:pk>/', SubTaskDetailUpdateDeleteView.as_view(), name='subtask-detail'),
]
