from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Voter(models.Model):
    # admin = models.OneToOneField(User, on_delete=models.CASCADE)
    user = models.ForeignKey('auth.User', related_name='api_voter_admin', on_delete=models.CASCADE)
    verified = models.BooleanField(default=True)
    voted = models.BooleanField(default=False)

    def __str__(self):
        return self.user.email


class Position(models.Model):
    name = models.CharField(max_length=50, unique=True)
    max_vote = models.IntegerField()
    priority = models.IntegerField()

    def __str__(self):
        return self.name


class Candidate(models.Model):
    fullname = models.CharField(max_length=50)
    photo = models.ImageField(upload_to="media/candidates")
    bio = models.TextField()
    position = models.ForeignKey(Position, on_delete=models.CASCADE)

    def __str__(self):
        return self.fullname


class Vote(models.Model):
    voter = models.ForeignKey(Voter, on_delete=models.CASCADE)
    position = models.ForeignKey(Position, on_delete=models.CASCADE)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)

    def __str__(self):
        return self.voter.email