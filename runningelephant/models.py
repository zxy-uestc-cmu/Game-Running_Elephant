from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.
class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    img = models.ImageField(blank=True, null=True, upload_to='./')
    age = models.IntegerField(validators=[MinValueValidator(0)], blank=True, null=True)
    starsign = models.CharField(max_length=20, blank=True, null=True)
    friends = models.ManyToManyField('self', blank=True, null=True)
    def __str__(self):
        return self.user.username
    

class Score(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    score = models.IntegerField(validators=[MinValueValidator(0)])
    time = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.player.user.username) + " " + str(self.score)


class Thoughts(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    thoughts = models.CharField(max_length=140, blank=True, null=True)
