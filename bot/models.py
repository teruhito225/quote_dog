from django.db import models

class Quote(models.Model):
    category = models.CharField(max_length=100)
    text = models.TextField()
    human = models.CharField(max_length=100)

    def __str__(self):
        return self.text