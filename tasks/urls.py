from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    CategoryListCreate, CategoryDetail,
    TaskViewSet, TaskListCreateAPIView, TaskRetrieveUpdateDestroyAPIView,
    SubTaskListCreateAPIView, SubTaskRetrieveUpdateDestroyAPIView,
    TaskStatisticsAPIView,
    RegisterView, LogoutView, CustomTokenObtainPairView
)

router = DefaultRouter()
router.register(r'task-viewset', TaskViewSet, basename='task-viewset')

urlpatterns = [

    path('categories/', CategoryListCreate.as_view(), name='category-list-create'),
    path('categories/<int:pk>/', CategoryDetail.as_view(), name='category-detail'),


    path('tasks/', TaskListCreateAPIView.as_view(), name='task-list-create'),
    path('tasks/<int:pk>/', TaskRetrieveUpdateDestroyAPIView.as_view(), name='task-detail'),
    path('tasks/statistics/', TaskStatisticsAPIView.as_view(), name='task-statistics'),


    path('subtasks/', SubTaskListCreateAPIView.as_view(), name='subtask-list-create'),
    path('subtasks/<int:pk>/', SubTaskRetrieveUpdateDestroyAPIView.as_view(), name='subtask-detail'),

    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),


    path('', include(router.urls)),
]




