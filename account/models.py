from django.db import models
from django.contrib.auth.models import User
# django amaderke built in user niye kaj korar facility dey

class CustomUser(models.Model):
    ACCOUNT_TYPE = (("admin", "Admin"), ("voter", "Voter"))
    user = models.OneToOneField(User, related_name='account', on_delete=models.CASCADE)
    email = models.EmailField(unique=True)
    birth_date = models.DateField(null=True, blank=True)
    user_type = models.CharField(default="voter", choices=ACCOUNT_TYPE, max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email