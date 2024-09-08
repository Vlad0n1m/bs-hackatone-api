from django.db import models

class Quiz(models.Model):
    link = models.URLField(max_length=200)
    title = models.CharField(max_length=255)
    description = models.TextField()
    cover_image = models.ImageField(upload_to='covers/', blank=True, null=True)

    def __str__(self):
        return self.title