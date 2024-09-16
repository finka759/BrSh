from django.urls import path

from content_app.apps import ContentAppConfig
from content_app.views import CourseListView, TeacherCourseCreateView, TeacherCourseDeleteView, \
    TeacherCourseListView, TeacherCourseUpdateView, TeacherCourseDetailView, TeacherModuleUpdateView, \
    TeacherLessonUpdateView, TeacherStepUpdateView, TeacherModuleDeleteView, TeacherModuleCreateView, \
    TeacherStepDeleteView, StudentCourseListView, CourseDetailView, course_confirm_subscription, \
    StudentCourseDetailView, StudentStepDetailView, FreeCourseDetailView, FreeStepDetailView




app_name = ContentAppConfig.name

urlpatterns = [
    path('', CourseListView.as_view(), name='index'),
    path('course_list_published', CourseListView.as_view(), name='course_list_published'),
    path('course/<int:pk>/', CourseDetailView.as_view(), name='course_detail'),

    path('free/course/<int:pk>/', FreeCourseDetailView.as_view(), name='free_course_detail'),
    path('free/step/<int:pk>/', FreeStepDetailView.as_view(), name='free_step_detail'),

    path('teacher/course/<int:pk>/delete/', TeacherCourseDeleteView.as_view(), name='teacher_course_delete'),
    path('teacher/course/create/', TeacherCourseCreateView.as_view(), name='teacher_course_create'),
    path('teacher/course/<int:pk>/update/', TeacherCourseUpdateView.as_view(), name='teacher_course_update'),
    path('teacher/course_list/', TeacherCourseListView.as_view(), name='teacher_course_list'),
    path('teacher/course/<int:pk>/', TeacherCourseDetailView.as_view(), name='teacher_course_detail'),
    path('teacher/module/<int:pk>/update/', TeacherModuleUpdateView.as_view(), name='teacher_module_update'),
    path('teacher/lesson/<int:pk>/update/', TeacherLessonUpdateView.as_view(), name='teacher_lesson_update'),
    path('teacher/step/<int:pk>/update/', TeacherStepUpdateView.as_view(), name='teacher_step_update'),
    path('teacher/module/<int:pk>/delete/', TeacherModuleDeleteView.as_view(), name='module_delete'),
    path('teacher/module/create/', TeacherModuleCreateView.as_view(), name='teacher_module_form'),
    path('teacher/step/<int:pk>/delete/', TeacherStepDeleteView.as_view(), name='step_delete'),

    path('student/course_list/', StudentCourseListView.as_view(), name='student_course_list'),
    path('student/confirm_subscription/<int:pk>/', course_confirm_subscription, name='course_confirm_subscription'),
    path('student/course/<int:pk>/', StudentCourseDetailView.as_view(), name='student_course_detail'),

    path('student/step/<int:pk>/', StudentStepDetailView.as_view(), name='student_step_detail'),
]
