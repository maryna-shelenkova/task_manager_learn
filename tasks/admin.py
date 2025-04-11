# from django.contrib import admin
# from .models import Task, SubTask, Category
#
# admin.site.register(Task)
# admin.site.register(SubTask)
# admin.site.register(Category)

from django.contrib import admin
from .models import Task, SubTask, Category

class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'created_at', 'deadline')
    search_fields = ('title', 'description')
    list_filter = ('status', 'created_at', 'categories')
    ordering = ['-created_at']

class SubTaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'task', 'status', 'created_at', 'deadline')
    search_fields = ('title', 'description')
    list_filter = ('status', 'created_at')
    ordering = ['-created_at']

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ['name']

admin.site.register(Task, TaskAdmin)
admin.site.register(SubTask, SubTaskAdmin)
admin.site.register(Category, CategoryAdmin)

