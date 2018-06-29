from django.db import models


class AbstractDateTimeModel(models.Model):
    creation_datetime = models.DateTimeField(auto_now_add=True)
    last_update_datetime = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.full_clean()
        super(AbstractDateTimeModel, self).save(*args, **kwargs)
