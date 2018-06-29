from django.db import models

from grpc_book_service.models.abstract_date_time import AbstractDateTimeModel


class Book(AbstractDateTimeModel):
    title = models.CharField(max_length=128, unique=True)
    isbn = models.IntegerField(unique=True)
    name = models.CharField(max_length=256, null=True)
    author = models.ForeignKey('grpc_book_service.Author',
                               related_name='books')
    book_type = models.CharField(max_length=64, choices=(
        ("PAPER_BACK", "Paper-Back",),
        ("HARD_BIND", "Hard Cover",),
        ("ONLINE", "Online",),))

    metadata_ref = models.TextField(null=True, blank=True)
    publication = models.TextField()

    class Meta(object):
        app_label = 'grpc_book_service'

    def __str__(self):
        return "<Book: {key}-{value}>".format(
            key=self.id,
            value=self.title
        )

    def __unicode__(self):
        return self.__str__()
