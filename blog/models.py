from django.db import models
from django.db.models import Avg
from users.models import Profile
class Article(models.Model):
    content = models.TextField()  # Use TextField for Markdown content
    title = models.CharField(max_length=255)
    date = models.DateField()
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='articles')

    def __str__(self):
        return self.title

    def get_average_rating(self):
        avg_rating = self.articlerating_set.aggregate(average=Avg('rating'))['average']
        return avg_rating if avg_rating is not None else 0

class ArticleRating(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='article_ratings')
    rating = models.IntegerField()

    def __str__(self):
        return f'{self.article.title} - {self.rating}'

    def save(self, *args, **kwargs):
        if self.rating < 0:
            self.rating = 0
        elif self.rating > 5:
            self.rating = 5
        super().save(*args, **kwargs)