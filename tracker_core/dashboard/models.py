import uuid

from django.db import models


class Dataset(models.Model):
    """
    'Dataset' class has been initially designed as identifier of a dataset.
    It is planned that users will use pre-defined datasets (SUPPLIES, UTILITIES, HOME_ROUTINE, OTHER)
    as well as create their own.
    """
    dataset = models.CharField(
        null=False,
        blank=False,
        max_length=255,
        default='OTHER',
        help_text='You can use pre-defined dataset type (SUPPLIES, UTILITIES, HOME_ROUTINE, OTHER) or create your own',
    )
    description = models.CharField(
        null=False,
        blank=False,
        max_length=255,
        default='This is dataset description.',
        help_text='You can describe the dataset purpose or any other valuable details',
    )

    def __str__(self):
        return self.dataset


class CoreObject(models.Model):
    """
    Core model that has all required fields to reflect SMART concept, namely:
    - Specific (id, name, description, obj_type)
    - Measurable (measure, _measure_limit, measure_unit)
    - Assignable (responsible)
    - Realistic (status)
    - Time-related (lifelong_period)
    """

    class StatusChoices(models.TextChoices):
        """
        Choices for 'status' field.
        Initially designed as simple colored 'success-warning-danger' pattern for dashboards
        """
        GREEN = 'G'
        ORANGE = 'O'
        RED = 'R'

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    name = models.CharField(
        null=False,
        blank=False,
        max_length=255,
    )
    description = models.CharField(
        null=False,
        blank=False,
        max_length=255,
    )
    """
    Identifier of object's relation to appropriate dataset 
    """
    dataset = models.ForeignKey(
        Dataset,
        on_delete=models.CASCADE,
        default='OTHER',
    )
    """
    'measure' field defines quantity if such applicable.
    Otherwise it should be set as '1', or '2', or '3' reflecting Red-Orange-Green model.
    """
    measure = models.IntegerField(
        null=False,
        blank=False,
        default=0,
        help_text='If not set, 1-Green, 2-Orange, 3-Red',
    )
    """
    'measure_limit' field is designed as a frames to evaluate the object's status
    by comparing the 'measure_limit' with current 'measure' value
    """
    measure_limit = models.IntegerField(
        null=False,
        blank=False,
        verbose_name='Measure limit'

    )
    measure_unit = models.CharField(
        null=False,
        blank=False,
        max_length=255,
        default='unit',
    )
    status = models.CharField(
        null=False,
        blank=False,
        max_length=255,
        choices=StatusChoices.choices,
        default=StatusChoices.GREEN
    )
    lifelong_period = models.IntegerField(
        null=False,
        blank=False,
    )
    responsible = models.CharField(
        null=False,
        blank=False,
        max_length=255,
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('coreobject-detail', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['status', 'dataset', 'responsible', 'name']
