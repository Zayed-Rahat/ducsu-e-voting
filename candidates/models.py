from django.db import models

# Create your models here.
class Position(models.Model):
    name = models.CharField(max_length=50, unique=True)
    max_vote = models.IntegerField()
    priority = models.IntegerField()
    def __str__(self):
        return self.name
   
class Candidate(models.Model):
    full_name = models.CharField(max_length=60)
    photo = models.ImageField(upload_to='images/candidates')
    bio = models.TextField()
    position = models.ForeignKey(Position, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.full_name