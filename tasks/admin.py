from django.contrib import admin
from tasks.models import Task, Category


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('short_title', 'created_at')
    search_fields = ('title', 'description')
    ordering = ['-created_at']

    def short_title(self, obj):
        return obj.title if len(obj.title) <= 10 else obj.title[:10] + '...'
    short_title.short_description = 'Title'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ['name']
