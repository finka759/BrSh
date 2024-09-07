from django.db import models

from users.models import User

NULLABLE = {"blank": True, "null": True}


class Course(models.Model):
    name = models.CharField(
        max_length=128,
        verbose_name="название курса",
    )
    description = models.TextField(
        verbose_name="описание учебного курса",
        **NULLABLE,
    )
    image = models.ImageField(
        upload_to="course/images/",
        verbose_name="изображение",
        **NULLABLE,
    )
    is_published = models.BooleanField(
        default=False,
    )

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='владелец',
        **NULLABLE,
    )

    class Meta:
        ordering = ['name']
        verbose_name = "учебный курс"
        verbose_name_plural = "учебные курсы"

    def __str__(self):
        return (
            f"наименование курса: {self.name}"
        )


class Module(models.Model):
    ordering_number = models.PositiveSmallIntegerField(
        verbose_name="порядковый номер",
    )
    name = models.CharField(
        max_length=128,
        verbose_name="название модуля",
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE
    )

    class Meta:
        ordering = ['ordering_number']
        verbose_name = "учебный модуль"
        verbose_name_plural = "учебные модули"

    def __str__(self):
        return (
            f"наименование модуля: {self.name}"
        )


class Lesson(models.Model):
    name = models.CharField(
        max_length=128,
        verbose_name="название урока",
    )
    module = models.ForeignKey(
        Module,
        on_delete=models.CASCADE
    )
    ordering_number = models.PositiveSmallIntegerField(
    )  # порядковый номер в урока в модуле

    class Meta:
        ordering = ['ordering_number']
        verbose_name = "урок"
        verbose_name_plural = "уроки"

    def __str__(self):
        return (
            f"наименование урока: {self.name}"
        )


# Шаг
class Step(models.Model):
    name = models.CharField(
        max_length=128,
        verbose_name="название шага",
    )
    content = models.TextField(
        verbose_name="контент шага",
        **NULLABLE,
    )
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE
    )
    ordering_number = models.PositiveSmallIntegerField(
    )  # порядковый номер в шага в уроке

    class Meta:
        ordering = ['ordering_number']
        verbose_name = "шаг"
        verbose_name_plural = "шаги"

    def __str__(self):
        return (
            f"наименование шага: {self.name}"
        )
