from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import inlineformset_factory
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from content_app.forms import TeacherCourseForm, TeacherModuleForm, TeacherLessonForm, TeacherStepForm
from content_app.models import Course, Module, Lesson, Step


class CourseListView(ListView):
    model = Course
    template_name = "content_app/course_list_published.html"

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(is_published=True)
        return qs


class TeacherCourseListView(ListView):
    model = Course
    template_name = "content_app/teacher_course_list.html"

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(owner=self.request.user)
        return qs


class TeacherCourseDetailView(DetailView):
    model = Course
    template_name = "content_app/teacher_course_detail.html"


class TeacherCourseCreateView(CreateView, LoginRequiredMixin):
    model = Course
    form_class = TeacherCourseForm
    template_name = "content_app/teacher_course_form.html"
    success_url = reverse_lazy("content_app:index")

    def form_valid(self, form):
        course = form.save()
        course.owner = self.request.user
        course.save()
        return super().form_valid(form)


class TeacherCourseUpdateView(UpdateView):
    model = Course
    form_class = TeacherCourseForm
    template_name = "content_app/teacher_course_form.html"
    success_url = reverse_lazy("content_app:index")

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        TeacherModuleFormset = inlineformset_factory(Course, Module, form=TeacherModuleForm, extra=1)
        if self.request.method == 'POST':
            context_data["formset"] = TeacherModuleFormset(self.request.POST, instance=self.object)
        else:
            context_data["formset"] = TeacherModuleFormset(instance=self.object)
        return context_data

    def form_valid(self, form):
        context_data = self.get_context_data()
        formset = context_data["formset"]
        if form.is_valid() and formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return super().form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form, formset=formset))


class CourseDeleteView(DeleteView):
    model = Course
    success_url = reverse_lazy("content_app:index")


# class TeacherCourseModuleListView(ListView):
#     model = Course
#     template_name = "content_app/teacher/course/module_list.html"
#
#     def get_queryset(self, *args, **kwargs):
#         qs = super().get_queryset(*args, **kwargs)
#         qs = qs.filter(course=self.request.course)
#         return qs
class TeacherModuleUpdateView(UpdateView):
    model = Module
    form_class = TeacherModuleForm
    template_name = "content_app/teacher_module_form.html"
    success_url = reverse_lazy("content_app:index")

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        TeachereLessonFormset = inlineformset_factory(Module, Lesson, form=TeacherLessonForm, extra=1)
        if self.request.method == 'POST':
            context_data["formset"] = TeachereLessonFormset(self.request.POST, instance=self.object)
        else:
            context_data["formset"] = TeachereLessonFormset(instance=self.object)
        return context_data

    def form_valid(self, form):
        context_data = self.get_context_data()
        formset = context_data["formset"]
        if form.is_valid() and formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return super().form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form, formset=formset))


class TeacherLessonUpdateView(UpdateView):
    model = Lesson
    form_class = TeacherLessonForm
    template_name = "content_app/teacher_lesson_form.html"
    success_url = reverse_lazy("content_app:index")

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        TeacherStepFormset = inlineformset_factory(Lesson, Step, form=TeacherStepForm, extra=1)
        if self.request.method == 'POST':
            context_data["formset"] = TeacherStepFormset(self.request.POST, instance=self.object)
        else:
            context_data["formset"] = TeacherStepFormset(instance=self.object)
        return context_data

    def form_valid(self, form):
        context_data = self.get_context_data()
        formset = context_data["formset"]
        if form.is_valid() and formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return super().form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form, formset=formset))


class TeacherStepUpdateView(UpdateView):
    model = Step
    form_class = TeacherStepForm
    template_name = "content_app/teacher_step_form.html"
    success_url = reverse_lazy("content_app:index")
