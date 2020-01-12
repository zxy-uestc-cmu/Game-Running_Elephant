from django.contrib import admin
from .models import Player,Score, Thoughts
from django.contrib.auth.models import User

# Register your models here.
admin.site.register([Player,Score,Thoughts])
