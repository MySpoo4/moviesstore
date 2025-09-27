from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Petition(models.Model):
    id = models.AutoField(primary_key=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    title = models.CharField(max_length=255)
    description = models.TextField()

    votes = models.ManyToManyField(User, related_name="petition_votes")

    def __str__(self):
        return str(self.id) + " - " + self.title
