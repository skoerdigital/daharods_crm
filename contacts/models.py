from django.db import models
from django.core.urlresolvers import reverse
from django.conf import settings

User = settings.AUTH_USER_MODEL

# Create your models here.
class Contact(models.Model):
    owner = models.ForeignKey(User)
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=50)
    email = models.CharField(max_length=30, blank = True, null = True)
    tel = models.CharField(max_length=30, blank = True, null = True)
    is_appointed = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('contacts:detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.name + ' ' + self.surname