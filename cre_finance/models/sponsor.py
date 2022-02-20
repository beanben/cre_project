from django.db import models


class Sponsor(models.Model):
    name = models.CharField(blank=True, max_length=100)

    def __str__(self):
        return self.name
