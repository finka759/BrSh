from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import inlineformset_factory
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from content_app.forms import TeacherCourseForm, TeacherModuleForm, TeacherLessonForm, TeacherStepForm, \
    TeacherStepForSetForm
from content_app.models import Course, Module, Lesson, Step
from users.models import User


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
    success_url = reverse_lazy("content_app:teacher_course_list")

    def form_valid(self, form):
        course = form.save()
        course.owner = self.request.user
        course.save()
        return super().form_valid(form)


class TeacherCourseUpdateView(UpdateView):
    model = Course
    form_class = TeacherCourseForm
    template_name = "content_app/teacher_course_form.html"

    def get_success_url(self):
        return reverse_lazy("content_app:teacher_course_update", kwargs={"pk": self.object.pk})

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
    success_url = reverse_lazy("content_app:teacher_course_list")


class TeacherModuleUpdateView(UpdateView):
    model = Module
    form_class = TeacherModuleForm
    template_name = "content_app/teacher_module_form.html"

    def get_success_url(self):
        return reverse_lazy("content_app:teacher_course_detail", kwargs={"pk": self.object.course.id})

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

    def get_success_url(self):
        return reverse_lazy("content_app:teacher_course_detail", kwargs={"pk": self.object.module.course.id})

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        TeacherStepFormset = inlineformset_factory(Lesson, Step, form=TeacherStepForSetForm, extra=1)
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
    success_url = reverse_lazy("content_app:teacher_course_list")

    def get_success_url(self):
        return reverse_lazy("content_app:teacher_course_detail", kwargs={"pk": self.object.lesson.module.course.id})


class TeacherModuleDeleteView(DeleteView):
    model = Module
    success_url = reverse_lazy("content_app:teacher_course_list")


class TeacherModuleCreateView(CreateView, LoginRequiredMixin):
    model = Module
    form_class = TeacherModuleForm
    template_name = "content_app/teacher_module_form.html"
    success_url = reverse_lazy("content_app:teacher_course_list")


class TeacherStepDeleteView(DeleteView):
    model = Step
    success_url = reverse_lazy("content_app:teacher_course_list")


class StudentCourseListView(ListView):
    model = Course
    template_name = "content_app/student_course_list.html"

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(studying_users=self.request.user)
        return qs


class CourseDetailView(DetailView):  # страница предпросмотра для выбора к обучению
    model = Course
    template_name = "content_app/course_detail.html"


def course_confirm_subscription(request, pk):
    course = get_object_or_404(Course, pk=pk)
    context = {"object": course}
    if request.method == 'POST':
        if request.POST.get('start_course'):
            course.studying_users.add(request.user)
            course.save()
        if request.POST.get('stop_course'):
            course.studying_users.remove(request.user)
            course.save()
        return redirect('content_app:student_course_list')
    return render(request, 'content_app/course_confirm_subscription.html', context)


class StudentCourseDetailView(DetailView):
    model = Course
    template_name = "content_app/student_course_detail.html"


class StudentLessonDetailView(DetailView):
    model = Lesson
    template_name = "content_app/student_lesson_detail.html"


class StudentStepDetailView(DetailView):
    model = Step
    template_name = "content_app/student_step_detail.html"

    def get_object(self, queryset=None, ):
        self.object = super().get_object(queryset)
        user = self.request.user
        self.object.steps_used_users.add(user)
        self.object.save()
        return self.object


class FreeCourseDetailView(DetailView):
    model = Course
    template_name = "content_app/free_course_detail.html"


class FreeStepDetailView(DetailView):
    model = Step
    template_name = "content_app/free_step_detail.html"


