from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver



class Voter(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    verified = models.BooleanField(default=True)
    voted = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_voter(sender, instance, created, **kwargs):
    if created:
        Voter.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_voter(sender, instance, **kwargs):
    instance.voter.save()


class Position(models.Model):
    name = models.CharField(max_length=50, unique=True)
    max_vote = models.IntegerField()
    priority = models.IntegerField()
    position_title = models.CharField(max_length=100, null=True)

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
        return self.voter.user.username
    


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)