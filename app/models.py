from django.db import models
from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(default='', null=False)

    def __str__(self):
        return f"{self.name}"


class UserPreference(models.Model):
    types = [
        ('Video', 'Video'),
        ('Audio', 'Audio'),
        ('Text', 'Text'),

    ]

    interests = models.TextField()
    preferred_type_of_studying = models.CharField(choices=types)
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=1)


class Plan(models.Model):
    description = models.TextField()


class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)


class TestResult(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    result = models.TextField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)


class PersonalCourse(models.Model):
    COURSE_TYPES = [
        ('Video', 'Video'),
        ('Audio', 'Audio'),
        ('Text', 'Text'),
    ]

    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    plan = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=255, choices=COURSE_TYPES, default='Video')


class Lesson(models.Model):
    personal_course = models.ForeignKey(PersonalCourse, on_delete=models.CASCADE)
    title = models.CharField(max_length=300)
    text = models.TextField(null=True, blank=True)
    video_links = models.TextField(null=True, blank=True)
    image_links = models.TextField(null=True, blank=True)
    audio = models.FileField(upload_to="audio/lessons/", null=True, blank=True)




class BrainBytes(models.Model):
    video = models.FileField(upload_to="videos/brain-bytes/", validators=[FileExtensionValidator(allowed_extensions=["mp4", "avif"])], blank=False, null=False)
    description = models.TextField()
    hashtags = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.PositiveIntegerField(default=0)
    shares = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)


class CommentsB(models.Model):
    video = models.ForeignKey(BrainBytes, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.PositiveIntegerField(default=0)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    likes = models.PositiveIntegerField(default=0)
    shares = models.PositiveIntegerField(default=0)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)


class Research(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField(null=True, blank=True)
    file = models.FileField(upload_to="files/community/", validators=[FileExtensionValidator(allowed_extensions=["pdf", "txt"])], blank=True, null=True)
    public = models.BooleanField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)


class Cooperation(models.Model):
    title = models.CharField(max_length=255)
    people_quantity = models.PositiveIntegerField(default=1)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    searching_people = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)


class CommentsC(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.PositiveIntegerField(default=0)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    

