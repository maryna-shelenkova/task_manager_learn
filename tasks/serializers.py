from .models import Task, SubTask, Category
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator


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
            except Exception:
                return text

        if 'title' in data:
            data['title'] = remove_non_ascii(data['title'])
        if 'description' in data:
            data['description'] = remove_non_ascii(data['description'])
        return data


class TaskStatisticsSerializer(serializers.Serializer):
    completed_tasks = serializers.IntegerField()
    pending_tasks = serializers.IntegerField()

class SubTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTask
        fields = ['id', 'title', 'description', 'status', 'deadline', 'task', 'owner']
        read_only_fields = ['owner']




class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all(), message="Email уже используется")]
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        style={'input_type': 'password'}
    )
    password2 = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2')
        extra_kwargs = {
            'username': {
                'validators': [UniqueValidator(queryset=User.objects.all(), message="Имя пользователя уже существует")]
            }
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({'password': "Пароли не совпадают"})
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data.update({'username': self.user.username})
        return data





