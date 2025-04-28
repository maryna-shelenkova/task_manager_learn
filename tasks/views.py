from django.core.paginator import Paginator
from django.http import JsonResponse
from .models import Task, SubTask
from datetime import datetime



def tasks_by_weekday(request):
    weekday = request.GET.get('weekday', None)

    if weekday:
        weekday_num = datetime.strptime(weekday, '%A').weekday()  # 0 - Monday, 6 - Sunday
        tasks = Task.objects.filter(deadline__week_day=weekday_num + 1)  # В Django неделя начинается с воскресенья (1)
    else:
        tasks = Task.objects.all()


    task_data = [
        {"title": task.title, "description": task.description, "status": task.status, "deadline": task.deadline} for
        task in tasks]
    return JsonResponse(task_data, safe=False)


def subtasks_list(request):

    subtasks = SubTask.objects.all().order_by('-created_at')

    paginator = Paginator(subtasks, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    subtask_data = [{"title": subtask.title, "description": subtask.description, "status": subtask.status,
                     "deadline": subtask.deadline} for subtask in page_obj]
    return JsonResponse(subtask_data, safe=False)


def subtasks_by_task_and_status(request):
    task_title = request.GET.get('task_title', None)
    status = request.GET.get('status', None)


    subtasks = SubTask.objects.all()

    if task_title:
        subtasks = subtasks.filter(task__title__icontains=task_title)

    if status:
        subtasks = subtasks.filter(status=status)

    paginator = Paginator(subtasks, 5)


    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)


    subtask_data = [{"title": subtask.title, "description": subtask.description, "status": subtask.status,
                     "deadline": subtask.deadline} for subtask in page_obj]
    return JsonResponse(subtask_data, safe=False)

