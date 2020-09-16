from django.db import models


class Task(models.Model):
    """Задача."""

    class Statuses(models.IntegerChoices):
        TODO = 0
        IN_PROGRESS = 1
        DONE = 2

    id = models.SmallAutoField(primary_key=True)
    title = models.CharField(
        max_length=64,
        verbose_name='Заголовок'
    )
    start_time = models.DateTimeField(null=True)
    end_time = models.DateTimeField(null=True)
    status = models.PositiveSmallIntegerField(
        choices=Statuses.choices,
        default=0
    )
    payment = models.PositiveIntegerField(
        default=0
    )

    class Meta:
        db_table = 'tasks'
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'
