from django.contrib import admin

from content_app.models import Course, Module, Lesson, Step

admin.site.register(Lesson)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'image', 'is_published', 'owner')

@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'course', 'ordering_number')

@admin.register(Step)
class StepAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'content', 'lesson', 'ordering_number')
