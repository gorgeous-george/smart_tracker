import uuid

from django.db import models


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
        Initially designed as simple colored pattern for dashboards
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
        unique=True,
    )
    description = models.CharField(
        null=False,
        blank=False,
        max_length=255,
    )
    """
    'obj_type' field has been initially designed as identifier of a dataset.
    It is planned that users will use pre-defined datasets (SUPPLIES, UTILITIES, HOME_ROUTINE, OTHER)
    as well as create their own.
    """
    obj_type = models.CharField(
        null=False,
        blank=False,
        max_length=255,
        default='OTHER',
        help_text='You can use pre-defined dataset type (SUPPLIES, UTILITIES, HOME_ROUTINE, OTHER) or create your own',
    )
    measure = models.IntegerField(
        null=False,
        blank=False,
        default=0,
    )
    _measure_limit = models.IntegerField(
        null=False,
        blank=False,
    )
    measure_unit = models.CharField(
        null=False,
        blank=False,
        max_length=255,
        default='if not set, 1 is Green, 2 is Orange, 3 is Red'
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
