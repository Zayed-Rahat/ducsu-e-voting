from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Voter(models.Model):
    admin = models.OneToOneField(User, on_delete=models.CASCADE)
    verified = models.BooleanField(default=True)
    voted = models.BooleanField(default=False)

    def __str__(self):
        return self.admin.email


class Position(models.Model):
    name = models.CharField(max_length=50, unique=True)
    max_vote = models.IntegerField()
    priority = models.IntegerField()

    def __str__(self):
        return self.name


class Candidate(models.Model):
    position = models.ForeignKey(Position, on_delete=models.CASCADE)
    fullname = models.CharField(max_length=20)
    photo = models.ImageField(upload_to="candidates", blank=True)
    bio = models.TextField(max_length=50)
    def __str__(self):
        return self.fullname


class Vote(models.Model):
    voter = models.ForeignKey(Voter, on_delete=models.CASCADE)
    position = models.ForeignKey(Position, on_delete=models.CASCADE)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)

    def __str__(self):
        return self.voter.admin.email
