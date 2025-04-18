# from django.db import models
#
#
# class Category(models.Model):
#     name = models.CharField(max_length=100)
#
#     def __str__(self):
#         return self.name
#
#
# class Task(models.Model):
#     STATUS_CHOICES = [
#         ('New', 'New'),
#         ('In progress', 'In progress'),
#         ('Pending', 'Pending'),
#         ('Blocked', 'Blocked'),
#         ('Done', 'Done'),
#     ]
#
#     title = models.CharField(max_length=200)
#     description = models.TextField()
#     categories = models.ManyToManyField(Category, related_name='tasks')
#     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='New')
#     deadline = models.DateTimeField()
#     created_at = models.DateTimeField(auto_now_add=True)
#
#     class Meta:
#         unique_together = ('title', 'created_at')
#
#     def __str__(self):
#         return self.title
#
#
# class SubTask(models.Model):
#     STATUS_CHOICES = Task.STATUS_CHOICES
#
#     title = models.CharField(max_length=200)
#     description = models.TextField()
#     task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='subtasks')
#     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='New')
#     deadline = models.DateTimeField()
#     created_at = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return f"{self.title} ({self.task.title})"
#

from django.db import models
from django.contrib import admin



class Task(models.Model):
    STATUS_CHOICES = [
        ('New', 'New'),
        ('In progress', 'In progress'),
        ('Pending', 'Pending'),
        ('Blocked', 'Blocked'),
        ('Done', 'Done'),
    ]

    title = models.CharField(max_length=200, unique=True)
    description = models.TextField()
    categories = models.ManyToManyField('Category')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='New')
    deadline = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'task_manager_task'
        ordering = ['-created_at']
        verbose_name = 'Task'
        unique_together = ('title',)


class SubTask(models.Model):
    STATUS_CHOICES = [
        ('New', 'New'),
        ('In progress', 'In progress'),
        ('Pending', 'Pending'),
        ('Blocked', 'Blocked'),
        ('Done', 'Done'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='subtasks')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='New')
    deadline = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'task_manager_subtask'
        ordering = ['-created_at']
        verbose_name = 'SubTask'
        unique_together = ('title',)


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'task_manager_category'
        verbose_name = 'Category'
        unique_together = ('name',)



class TaskAdmin(admin.ModelAdmin):
    list_display = ('short_title', 'status', 'created_at', 'deadline')
    search_fields = ('title', 'description')
    list_filter = ('status', 'created_at', 'categories')
    ordering = ['-created_at']

    def short_title(self, obj):
        return obj.title[:10] + '...' if len(obj.title) > 10 else obj.title

    short_title.short_description = 'Title'



class SubTaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'task', 'status', 'created_at', 'deadline')
    search_fields = ('title', 'description')
    list_filter = ('status', 'created_at')
    ordering = ['-created_at']
    actions = ['mark_as_done']

    @admin.action(description='Отметить как выполненные')
    def mark_as_done(self, request, queryset):
        updated = queryset.update(status='Done')
        self.message_user(request, f'{updated} подзадач отмечено как выполненные.')



class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ['name']





