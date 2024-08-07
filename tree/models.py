from django.db import models
from django.urls import reverse


class Menu(models.Model):
    name = models.CharField(max_length=256, unique=True)

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    menu = models.ForeignKey(Menu, related_name='items', on_delete=models.CASCADE)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.CASCADE)
    name = models.CharField(max_length=256)
    url = models.CharField(max_length=256, blank=True)
    named_url = models.CharField(max_length=256, blank=True)

    def get_absolute_url(self):
        if self.url:
            return self.url
        if self.named_url:
            return reverse(self.named_url)
        return '#'

    def __str__(self):
        return self.name
