import uuid

from django.db import models
from django.conf import settings


class Dataset(models.Model):
    dataset = models.CharField(
        null=False,
        blank=False,
        max_length=255,
        help_text='Give a name to your dataset',
    )
    description = models.CharField(
        null=False,
        blank=False,
        max_length=255,
        help_text='Describe the dataset purpose or any other valuable details',
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        help_text='Current user name',
    )

    def __str__(self):
        return self.dataset


class CoreObject(models.Model):
    """
    Core model that has all required fields to reflect SMART concept, namely:
    - Specific (id, name, description, dataset)
    - Measurable (measure, measure_limit, measure_description)
    - Assignable (responsible)
    - Realistic (status)
    - Time-related (time_frame)
    """

    class GreenOrangeRedChoices(models.TextChoices):
        """
        Choices for 'Measure', 'Measure limit', 'Status' field.
        Initially designed as simple colored 'success-warning-danger' pattern for dashboards
        """
        GREEN = 'Green'
        ORANGE = 'Orange'
        RED = 'Red'

    class TimeFrameChoices(models.TextChoices):
        """
        Choices for 'Time Frame' field.
        """
        DAY = 'Day'
        WEEK = 'Week'
        MONTH = 'Month'
        YEAR = 'Year'

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    name = models.CharField(
        null=False,
        blank=False,
        max_length=255,
        help_text='Add the name of your task/goal/object',
    )
    description = models.CharField(
        null=False,
        blank=False,
        max_length=255,
        help_text='Add short description of your task/goal/object',
    )
    """
    Identifier of object's relation to appropriate dataset 
    """
    dataset = models.ForeignKey(
        Dataset,
        on_delete=models.CASCADE,
        help_text='Choose appropriate dataset for this task/goal/object',
    )
    measure = models.CharField(
        null=False,
        blank=False,
        max_length=6,
        choices=GreenOrangeRedChoices.choices,
        default=GreenOrangeRedChoices.GREEN,
        help_text='Evaluate level of implementation by 3 levels according to measure description of your '
                  'task/goal/object',
    )
    """
    'measure_limit' field is designed as minimum satisfying level to evaluate the object's status
    by comparing the 'measure_limit' with current 'measure' value
    """
    measure_limit = models.CharField(
        null=False,
        blank=False,
        max_length=6,
        choices=GreenOrangeRedChoices.choices,
        default=GreenOrangeRedChoices.ORANGE,
        help_text='Choose minimum satisfying level of your task/goal/object status',
    )
    measure_description = models.CharField(
        null=False,
        blank=False,
        max_length=255,
        default='If not set, 1-Green, 2-Orange, 3-Red',
        help_text='Describe you 3-level pattern for evaluation of your task/goal/object.'
                  'Based on these 3 levels the task/goal/object would have appropriate'
                  'position/color at the chart',
    )
    status = models.CharField(
        null=False,
        blank=False,
        max_length=6,
        choices=GreenOrangeRedChoices.choices,
        default=GreenOrangeRedChoices.GREEN,
        help_text='Status of implementation/performing/achieving of your task/goal/object.'
                  'Status level is calculated comparing measure to measure limit.'
                  'Based on status level the task/goal/object would have appropriate'
                  'position/color at the chart',
    )
    timeframe = models.CharField(
        null=False,
        blank=False,
        max_length=5,
        choices=TimeFrameChoices.choices,
        default=TimeFrameChoices.DAY,
        help_text='Choose a deadline/timeframe of your task/goal/object implementation.'
    )
    responsible = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        help_text='Current user name',
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('coreobject-detail', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['status', 'dataset', 'responsible', 'name']
