from django.test import TestCase

from content_app.models import Course, Module, Lesson, Step
from users.models import User


class CourseTestCase(TestCase):

    def setUp(self):
        self.user1 = User.objects.create(email="user1@example.com")
        self.user2 = User.objects.create(email="user2@example.com")
        self.course1 = Course.objects.create(
            name='name_course_1',
            description='description_course_1',
            owner=self.user1
        )
        self.course2 = Course.objects.create(
            name='name_course_2',
            description='description_course_2',
            owner=self.user2
        )


    def test_course_detail(self):
        course = Course.objects.get(name="name_course_1")
        self.assertEqual(course.description, 'description_course_1')

    def test_course_list(self):
        course_count = Course.objects.all().count()
        self.assertEqual(course_count, 2)

    def test_course_update(self):
        course = Course.objects.get(name="name_course_1")
        course.description = 'description_for_course_1'
        self.assertEqual(course.description, 'description_for_course_1')

    def test_course_create(self):
        Course.objects.create(
            name='name_course_3',
            description='description_course_3',
            owner=self.user1
        )
        course_count = Course.objects.all().count()
        self.assertEqual(course_count, 3)

    def test_course_delete(self):
        course = Course.objects.get(name='name_course_2')
        course.delete()
        course_count = Course.objects.all().count()
        self.assertEqual(course_count, 1)


class ModuleTestCase(TestCase):

    def setUp(self):
        self.user1 = User.objects.create(email="user1@example.com")
        self.user2 = User.objects.create(email="user2@example.com")
        self.course1 = Course.objects.create(
            name='name_course_1',
            description='description_course_1',
            owner=self.user1
        )
        self.course2 = Course.objects.create(
            name='name_course_2',
            description='description_course_2',
            owner=self.user2
        )
        self.module1 = Module.objects.create(
            name='name_module_1',
            ordering_number=1,
            course=self.course1
        )
        self.module2 = Module.objects.create(
            name='name_module_2',
            ordering_number=2,
            course=self.course1
        )

    def test_module_detail(self):
        module = Module.objects.get(name="name_module_1")
        self.assertEqual(module.ordering_number, 1)

    def test_module_list(self):
        module_count = Module.objects.all().count()
        self.assertEqual(module_count, 2)

class LessonTestCase(TestCase):

    def setUp(self):
        self.user1 = User.objects.create(email="user1@example.com")
        self.user2 = User.objects.create(email="user2@example.com")
        self.course1 = Course.objects.create(
            name='name_course_1',
            description='description_course_1',
            owner=self.user1
        )
        self.course2 = Course.objects.create(
            name='name_course_2',
            description='description_course_2',
            owner=self.user2
        )
        self.module1 = Module.objects.create(
            name='name_module_1',
            ordering_number=1,
            course=self.course1
            )
        self.module2 = Module.objects.create(
            name='name_module_2',
            ordering_number=2,
            course=self.course1
        )
        self.lesson1 = Lesson.objects.create(
            name='name_lesson_1',
            ordering_number=1,
            module=self.module1
        )
        self.lesson2 = Lesson.objects.create(
            name='name_lesson_2',
            ordering_number=2,
            module=self.module1
        )
    def test_lesson_detail(self):
        lesson = Lesson.objects.get(name="name_lesson_1")
        self.assertEqual(lesson.ordering_number, 1)

    def test_module_list(self):
        lesson_count = Lesson.objects.all().count()
        self.assertEqual(lesson_count, 2)

    def test_lesson_update(self):
        lesson = Lesson.objects.get(name="name_lesson_1")
        lesson.ordering_number = 2
        self.assertEqual(lesson.ordering_number, 2)

    def test_lesson_create(self):
        Lesson.objects.create(
            name='name_lesson_3',
            ordering_number=3,
            module=self.module1
        )
        lesson_count = Lesson.objects.all().count()
        self.assertEqual(lesson_count, 3)

    def test_module_delete(self):
        lesson = Lesson.objects.get(name='name_lesson_2')
        lesson.delete()
        lesson_count = Lesson.objects.all().count()
        self.assertEqual(lesson_count, 1)


class StepTestCase(TestCase):

    def setUp(self):
        self.user1 = User.objects.create(email="user1@example.com")
        self.course1 = Course.objects.create(
            name='name_course_1',
            description='description_course_1',
            owner=self.user1
        )
        self.module1 = Module.objects.create(
            name='name_module_1',
            ordering_number=1,
            course=self.course1
            )
        self.lesson1 = Lesson.objects.create(
            name='name_lesson_1',
            ordering_number=1,
            module=self.module1
        )
        self.step1 = Step.objects.create(
            name='name_step_1',
            ordering_number=1,
            lesson=self.lesson1,
            content='content_step1'
        )
        self.step2 = Step.objects.create(
            name='name_step_2',
            ordering_number=2,
            lesson=self.lesson1,
            content='content_step2'
        )
    def test_step_detail(self):
        step = Step.objects.get(content='content_step1')
        self.assertEqual(step.ordering_number, 1)

    def test_step_list(self):
        step_count = Step.objects.all().count()
        self.assertEqual(step_count, 2)

    def test_step_update(self):
        step = Step.objects.get(name="name_step_1")
        step.ordering_number = 2
        self.assertEqual(step.ordering_number, 2)

    def test_step_create(self):
        Step.objects.create(
            name='name_step_3',
            ordering_number=3,
            lesson=self.lesson1
        )
        step_count = Step.objects.all().count()
        self.assertEqual(step_count, 3)

    def test_step_delete(self):
        step = Step.objects.get(name='name_step_2')
        step.delete()
        step_count = Step.objects.all().count()
        self.assertEqual(step_count, 1)

