from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.conf import settings
from .models import Task



@receiver(pre_save, sender=Task)
def notify_status_change(sender, instance, **kwargs):
    if not instance.pk:
        return

    try:
        old_instance = Task.objects.get(pk=instance.pk)
    except Task.DoesNotExist:
        return

    old_status = old_instance.status
    new_status = instance.status

    if old_status != new_status:
        email = instance.owner.email
        if email:  # Проверка на наличие email
            subject = f'Your task "{instance.title}" has changed status'
            message = (
                f'Hello {instance.owner.username},\n\n'
                f'Your task "{instance.title}" has changed status from "{old_status}" to "{new_status}".'
            )
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])



@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):
    if created:
        email = instance.email
        if email:
            send_mail(
                subject='Добро пожаловать!',
                message='Спасибо за регистрацию на нашем сайте.',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=False,
            )
