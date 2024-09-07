from django.urls import path

from content_app.apps import ContentAppConfig
from content_app.views import CourseListView, TeacherCourseCreateView, CourseDeleteView, \
    TeacherCourseListView, TeacherCourseUpdateView, TeacherCourseDetailView, TeacherModuleUpdateView, \
    TeacherLessonUpdateView, TeacherStepUpdateView

app_name = ContentAppConfig.name

urlpatterns = [
    path('', CourseListView.as_view(), name='index'),
    path('course_list_published', CourseListView.as_view(), name='course_list_published'),



    path('course/<int:pk>/delete/', CourseDeleteView.as_view(), name='course_delete'),

    path('teacher/course/create/', TeacherCourseCreateView.as_view(), name='teacher_course_create'),
    path('teacher/course/<int:pk>/update/', TeacherCourseUpdateView.as_view(), name='teacher_course_update'),

    path('teacher/course_list/', TeacherCourseListView.as_view(), name='teacher_course_list'),
    path('teacher/course/<int:pk>/', TeacherCourseDetailView.as_view(), name='teacher_course_detail'),
    path('teacher/module/<int:pk>/update/', TeacherModuleUpdateView.as_view(), name='teacher_module_update'),
    path('teacher/lesson/<int:pk>/update/', TeacherLessonUpdateView.as_view(), name='teacher_lesson_update'),
    path('teacher/step/<int:pk>/update/', TeacherStepUpdateView.as_view(), name='teacher_step_update'),




]
