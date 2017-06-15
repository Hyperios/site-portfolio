from django.db import models
from django.contrib.auth.models import User
import datetime

class PhotoTech(models.Model):
    ids = models.AutoField(primary_key=True)
    pub_date = models.DateTimeField('date published')
    name_model = models.CharField(max_length=200)
    image_url = models.FileField(max_length=100, upload_to='images/')
    available = models.IntegerField(default=0)
    price = models.CharField(default=0, blank=True)
    text_prev = models.CharField(max_length=500, blank=True)
    matrix_resol = models.CharField(max_length=50, blank=True)
    matrix_size = models.CharField(max_length=50, blank=True)
    max_resol = models.CharField(max_length=50, blank=True)
    zoom = models.CharField(max_length=50, blank=True)
    color = models.CharField(max_length=50, blank=True)
    country = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return str(self.ids)


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    activation_key = models.CharField(max_length = 40, blank = True)
    key_expires = models.DateTimeField(default = datetime.date.today())

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = u'User profiles'
