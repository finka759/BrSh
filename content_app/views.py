from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.forms import inlineformset_factory
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from content_app.forms import TeacherCourseForm, TeacherModuleForm, TeacherLessonForm, TeacherStepForm, \
    TeacherStepForSetForm
from content_app.models import Course, Module, Lesson, Step
from content_app.services import create_stripe_product, create_stripe_price, create_stripe_session
from users.models import Payment


class CourseListView(ListView):
    model = Course
    template_name = "content_app/course_list_published.html"

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(is_published=True)
        return qs


class TeacherCourseListView(ListView, LoginRequiredMixin):
    model = Course
    template_name = "content_app/teacher_course_list.html"

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(owner=self.request.user)
        return qs


class TeacherCourseDetailView(DetailView, LoginRequiredMixin):
    model = Course
    template_name = "content_app/teacher_course_detail.html"

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.request.user == self.object.owner:
            self.object.save()
            return self.object
        raise PermissionDenied


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


class TeacherCourseUpdateView(UpdateView, LoginRequiredMixin):
    model = Course
    form_class = TeacherCourseForm
    template_name = "content_app/teacher_course_form.html"

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.request.user == self.object.owner:
            self.object.save()
            return self.object
        raise PermissionDenied

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


class TeacherCourseDeleteView(DeleteView, LoginRequiredMixin):
    model = Course
    success_url = reverse_lazy("content_app:teacher_course_list")
    template_name = "content_app/teacher_course_confirm_delete.html"

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.request.user == self.object.owner:
            self.object.save()
            return self.object
        raise PermissionDenied


class TeacherModuleUpdateView(UpdateView, LoginRequiredMixin):
    model = Module
    form_class = TeacherModuleForm
    template_name = "content_app/teacher_module_form.html"

    def get_object(self, queryset=None, ):
        self.object = super().get_object(queryset)
        if self.request.user == self.object.course.owner:
            self.object.save()
            return self.object
        raise PermissionDenied

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


class TeacherLessonUpdateView(UpdateView, LoginRequiredMixin):
    model = Lesson
    form_class = TeacherLessonForm
    template_name = "content_app/teacher_lesson_form.html"

    def get_object(self, queryset=None, ):
        self.object = super().get_object(queryset)
        if self.request.user == self.object.module.course.owner:
            self.object.save()
            return self.object
        raise PermissionDenied

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


class TeacherStepUpdateView(UpdateView, LoginRequiredMixin):
    model = Step
    form_class = TeacherStepForm
    template_name = "content_app/teacher_step_form.html"
    success_url = reverse_lazy("content_app:teacher_course_list")

    def get_object(self, queryset=None, ):
        self.object = super().get_object(queryset)
        if self.request.user == self.object.lesson.module.course.owner:
            self.object.save()
            return self.object
        raise PermissionDenied

    def get_success_url(self):
        return reverse_lazy("content_app:teacher_course_detail", kwargs={"pk": self.object.lesson.module.course.id})


class TeacherModuleDeleteView(DeleteView, LoginRequiredMixin):
    model = Module
    success_url = reverse_lazy("content_app:teacher_course_list")

    def get_object(self, queryset=None, ):
        self.object = super().get_object(queryset)
        if self.request.user == self.object.course.owner:
            self.object.save()
            return self.object
        raise PermissionDenied


class TeacherModuleCreateView(CreateView, LoginRequiredMixin):
    model = Module
    form_class = TeacherModuleForm
    template_name = "content_app/teacher_module_form.html"
    success_url = reverse_lazy("content_app:teacher_course_list")


class TeacherStepDeleteView(DeleteView, LoginRequiredMixin):
    model = Step
    success_url = reverse_lazy("content_app:teacher_course_list")

    def get_object(self, queryset=None, ):
        self.object = super().get_object(queryset)
        if self.request.user == self.object.lesson.module.course.owner:
            self.object.save()
            return self.object
        raise PermissionDenied


class StudentCourseListView(ListView, LoginRequiredMixin):
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
    if not course.is_published:
        raise PermissionDenied
    context = {"object": course}
    if request.user.is_authenticated:  # проверка наличия оплаты курса данным пользователем
        paid = False
        pyment_set = course.payment_set.all()
        for pay in pyment_set:
            if pay.user == request.user and pay.course == course:
                paid = True
        context['paid'] = paid

        context['subscribed'] = course.studying_users.filter(id=request.user.id).exists()
        if request.method == 'POST':
            if request.POST.get('create_payment'):
                payment = Payment(user=request.user, course=course, summ=course.cost)
                payment.save()
                stripe_product_id = create_stripe_product(payment)
                price = create_stripe_price(summ=payment.summ, stripe_product_id=stripe_product_id)
                payment_id, payment_link = create_stripe_session(summ=price, pk=pk)
                payment.payment_id = payment_id
                payment.payment_link = payment_link
                payment.save()
                return redirect(payment_link, code=303)
            if request.POST.get('start_course'):
                course.studying_users.add(request.user)
                course.save()
                return redirect('content_app:student_course_list')
            if request.POST.get('stop_course'):
                course.studying_users.remove(request.user)
                course.save()
                return redirect('content_app:student_course_list')

    return render(request, 'content_app/course_confirm_subscription.html', context)


class StudentCourseDetailView(DetailView, LoginRequiredMixin):
    model = Course
    template_name = "content_app/student_course_detail.html"

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        user = self.request.user
        studying_users = self.object.studying_users.all()
        if user in studying_users:
            self.object.save()
            return self.object
        raise PermissionDenied


class StudentStepDetailView(DetailView, LoginRequiredMixin):
    model = Step
    template_name = "content_app/student_step_detail.html"

    def get_object(self, queryset=None, ):
        self.object = super().get_object(queryset)
        user = self.request.user
        studying_users = self.object.lesson.module.course.studying_users.all()
        if user in studying_users:  # доступ для просмотра только разрешенным пользователям
            self.object.steps_used_users.add(user)
            self.object.save()
            return self.object
        raise PermissionDenied


class FreeCourseDetailView(DetailView):
    model = Course
    template_name = "content_app/free_course_detail.html"


class FreeStepDetailView(DetailView):
    model = Step
    template_name = "content_app/free_step_detail.html"
