from rest_framework import serializers
from .models import Task, SubTask, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class TaskSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)
    category_ids = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Category.objects.all(), write_only=True, source='categories'
    )

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'deadline', 'categories', 'category_ids', 'owner']
        read_only_fields = ['owner']

    def validate(self, data):
        def remove_non_ascii(text):
            if not text:
                return text
            try:
                return text.encode('ascii', errors='ignore').decode()
            except Exception as e:
                print(f"Error cleaning text: {e}")
                return text

        data['title'] = remove_non_ascii(data.get('title', ''))
        data['description'] = remove_non_ascii(data.get('description', ''))
        return data

class SubTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTask
        fields = ['id', 'title', 'description', 'status', 'deadline', 'task', 'owner']
        read_only_fields = ['owner']


class TaskStatisticsSerializer(serializers.Serializer):
    total_tasks = serializers.IntegerField()
    completed_tasks = serializers.IntegerField()
    pending_tasks = serializers.IntegerField()




