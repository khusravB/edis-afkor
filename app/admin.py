from django.contrib import admin
from .models import *


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": "name"}


admin.site.register(Category)
admin.site.register(Plan)
admin.site.register(UserPreference)
admin.site.register(Course)
admin.site.register(PersonalCourse)
admin.site.register(TestResult)
admin.site.register(Lesson)
