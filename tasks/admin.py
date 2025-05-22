from django.contrib import admin
from django.db.models import QuerySet
from tasks.models import Task, SubTask, Category


class SubTaskInline(admin.TabularInline):
    model = SubTask
    extra = 1


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('short_title', 'status', 'created_at', 'deadline')
    search_fields = ('title', 'description')
    list_filter = ('status', 'created_at', 'categories')
    ordering = ['-created_at']
    inlines = [SubTaskInline]

    def short_title(self, obj):
        return obj.title if len(obj.title) <= 10 else obj.title[:10] + '...'
    short_title.short_description = 'Title'


@admin.action(description='Отметить выбранные подзадачи как Done')
def mark_as_done(modeladmin, request, queryset: QuerySet):
    updated = queryset.update(status='Done')
    modeladmin.message_user(request, f'Обновлено {updated} подзадач(и) в статус "Done".')


@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'task', 'status', 'created_at', 'deadline')
    search_fields = ('title', 'description')
    list_filter = ('status', 'created_at')
    ordering = ['-created_at']
    actions = [mark_as_done]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ['name']


