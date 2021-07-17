from django.db import models


class Room(models.Model):
    name = models.CharField(max_length=30)
    slug = models.CharField(max_length=50)

    def __str__(self):
        return self.name
