from django.contrib import admin
from django.db.models import QuerySet

from tasks.models import Task, SubTask, Category


class SubTaskInline(admin.StackedInline):
    model = SubTask
    extra = 1

@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    actions = ['set_subtask_status_to_done']
    list_display = ('task_title', 'title', 'description', 'deadline', 'status')

    def task_title(self, obj):
        return obj.task.title

    def set_subtask_status_to_done(self, request, queryset: QuerySet):
        updated = queryset.update(status="Done")
        self.message_user(request, f"Статус обновлен на 'Done' для {updated} подзадач.")

    set_subtask_status_to_done.short_description = "Обновить статусы на Done"

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    inlines = [SubTaskInline]
    list_display = ('short_title', 'description', 'categories_names', 'deadline', 'status')
    list_filter = ('title', 'categories__name', 'deadline', 'status')
    list_per_page = 5

    def short_title(self, obj: Task):
        return f"{obj.title[:10]}..." if len(obj.title) > 10 else obj.title

    def categories_names(self, obj: Task):
        return ", ".join([cat.name for cat in obj.categories.all()])

admin.site.register(Category)

