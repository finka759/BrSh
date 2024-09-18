from django import forms
from django.forms import BooleanField

from content_app.models import Course, Module, Lesson, Step


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, fild in self.fields.items():
            if isinstance(fild, BooleanField):
                fild.widget.attrs['class'] = 'form-check-input'
            else:
                fild.widget.attrs['class'] = 'form-control'


class TeacherCourseForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        ordering = ['ordering_number']
        model = Course
        fields = ("name", "description", "image", "is_published", "cost")


class TeacherModuleForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        ordering = ['ordering_number']
        model = Module
        fields = "__all__"


class TeacherLessonForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        ordering = ['ordering_number']
        model = Lesson
        fields = ('ordering_number', 'name')


class TeacherStepForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        ordering = ['ordering_number']
        model = Step
        fields = ('name', 'content')


class TeacherStepForSetForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        ordering = ['ordering_number']
        model = Step
        fields = ('ordering_number', 'name')
