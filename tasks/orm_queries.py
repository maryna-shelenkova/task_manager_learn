from datetime import timedelta
from django.utils import timezone
from tasks.models import Task, SubTask


task = Task.objects.create(
    title="Prepare presentation",
    description="Prepare materials and slides for the presentation",
    status="New",
    deadline=timezone.now() + timedelta(days=3),
)

SubTask.objects.create(
    title="Gather information",
    description="Find necessary information for the presentation",
    task=task,
    status="New",
    deadline=timezone.now() + timedelta(days=2),
)

SubTask.objects.create(
    title="Create slides",
    description="Create presentation slides",
    task=task,
    status="New",
    deadline=timezone.now() + timedelta(days=1),
)

print("\n✅ Создание завершено")


print("\n📋 Задачи со статусом 'New':")
for t in Task.objects.filter(status="New"):
    print(f"- {t.title}")

print("\n📋 Подзадачи со статусом 'Done' и просроченным дедлайном:")
for s in SubTask.objects.filter(status="Done", deadline__lt=timezone.now()):
    print(f"- {s.title} (для задачи '{s.task.title}')")


task.status = "In Progress"
task.save()

subtask1 = SubTask.objects.get(title="Gather information")
subtask1.deadline = timezone.now() - timedelta(days=2)
subtask1.save()

subtask2 = SubTask.objects.get(title="Create slides")
subtask2.description = "Create and format presentation slides"
subtask2.save()

print("\n✏️ Изменения сохранены")


Task.objects.filter(title="Prepare presentation").delete()
print("\n🗑️ Задача и связанные подзадачи удалены")

