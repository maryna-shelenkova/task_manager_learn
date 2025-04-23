from rest_framework import serializers
from .models import Task, SubTask, Category
from django.utils import timezone
from rest_framework.exceptions import ValidationError


class SubTaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTask
        fields = ['title', 'description', 'task', 'status', 'deadline', 'created_at']
        read_only_fields = ['created_at']

class CategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name']

    def validate_name(self, value):
        if Category.objects.filter(name=value).exists():
            raise serializers.ValidationError("Категория с таким именем уже существует.")
        return value

    def create(self, validated_data):
        return Category.objects.create(**validated_data)

    def update(self, instance, validated_data):
        new_name = validated_data.get('name', instance.name)
        if Category.objects.exclude(pk=instance.pk).filter(name=new_name).exists():
            raise serializers.ValidationError("Категория с таким именем уже существует.")
        instance.name = new_name
        instance.save()
        return instance


class SubTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTask
        fields = ['id', 'title', 'description', 'status', 'deadline', 'created_at']

class TaskDetailSerializer(serializers.ModelSerializer):
    subtasks = SubTaskSerializer(source='subtask_set', many=True, read_only=True)

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'deadline', 'created_at', 'subtasks']


class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['title', 'description', 'status', 'deadline']

    def validate_deadline(self, value):
        if value < timezone.now():
            raise ValidationError("Дедлайн не может быть в прошлом.")
        return value

