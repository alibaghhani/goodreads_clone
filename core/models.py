from django.db import models


class TimeStampMixin(models.Model):
    """
    timestamp mixin model for adding fields that related to time

    -----fields-----
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    expired_at = models.DateTimeField()
    """

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    expired_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        abstract = True
