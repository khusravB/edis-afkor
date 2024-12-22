from rest_framework import serializers
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from .models import *


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class BrainBytesSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = BrainBytes
        fields = ['id', 'video', 'description', 'hashtags', 'author', 'likes', 'shares', 'created_at']
        read_only_fields = ['likes', 'shares']

    def update(self, instance, validated_data):
        # Позволяем изменять likes и shares только при обновлении
        likes = validated_data.get('likes', instance.likes)
        shares = validated_data.get('shares', instance.shares)

        instance.likes = likes
        instance.shares = shares
        instance.save()

        return instance



class CommentsBSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = CommentsB
        fields = ['id', 'video', 'author', 'likes', 'content', 'created_at']
        read_only_fields = ['likes', 'created_at']


class PostSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Post
        fields = ['id', 'title', 'author', 'likes', 'content', 'created_at', 'shares']
        read_only_fields = ['likes', 'created_at', 'shares']


class ResearchSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Research
        fields = "__all__"
        read_only_fields = ['created_at']


class CooperationSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Cooperation
        fields = "__all__"
        read_only_fields = ['created_at']


class CommentsCSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = CommentsC
        fields = ['id', 'post', 'author', 'likes', 'content', 'created_at']
        read_only_fields = ['likes', 'created_at']


class ChatSerializer(serializers.Serializer):
    content = serializers.CharField(required=True, max_length=1000)

    def validate_content(self, value):
        if not value.strip():
            raise serializers.ValidationError("Message content cannot be empty.")
        return value


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'plan']


class PersonalCourseSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = PersonalCourse
        fields = ['id', 'course', 'created_at', 'plan', 'author', 'type']


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'personal_course', 'title', 'text', 'video_links', 'image_links', 'audio']

