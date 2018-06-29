from django.db import models

from grpc_book_service.models.abstract_date_time import AbstractDateTimeModel


class Author(AbstractDateTimeModel):
    author_name = models.CharField(max_length=128, unique=True)

    class Meta(object):
        app_label = 'grpc_book_service'

    def __str__(self):
        return "<Author: {key}-{value}>".format(
            key=self.id,
            value=self.author_name
        )

    def __unicode__(self):
        return self.__str__()
