from django.db import models
from django.db.models import Avg
from users.models import Profile

from django.utils.timezone import now
from datetime import timedelta


class Book(models.Model):
    ORIGINAL = 'Original'
    GIFTED = 'Gifted'
    
    ORIGIN_CHOICES = [
        (ORIGINAL, 'Original'),
        (GIFTED, 'Gifted'),
    ]

    GENRE_CHOICES = [
        ('Fiction', 'Fiction'),
        ('Non-fiction', 'Non-fiction'),
        ('Science Fiction', 'Science Fiction'),
        ('Fantasy', 'Fantasy'),
        ('Biography', 'Biography'),
        ('Mystery', 'Mystery'),
        ('Romance', 'Romance'),
        ('Horror', 'Horror'),
    ]

    title = models.CharField(max_length=255)
    desc = models.TextField()
    cover = models.ImageField(upload_to='covers/', blank=True, null=True)
    release_date = models.DateField()
    origin = models.CharField(max_length=8, choices=ORIGIN_CHOICES, default=ORIGINAL)
    genre = models.CharField(max_length=20, choices=GENRE_CHOICES)
    
    def __str__(self):
        return self.title

    def get_average_rating(self):
        avg_rating = self.bookrating_set.aggregate(average=Avg('rating'))['average']
        return avg_rating if avg_rating is not None else 0

class BookRating(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='book_ratings')
    rating = models.IntegerField()
    def __str__(self):
        return f'{self.book.title} - {self.rating}'

    def save(self, *args, **kwargs):
        if self.rating < 0:
            self.rating = 0
        elif self.rating > 5:
            self.rating = 5
        super().save(*args, **kwargs)


def default_deadline():
    return now() + timedelta(days=10)

class TakenBook(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='taken_books')

    date_taken = models.DateTimeField(default=now)  # Automatically set to now
    date_returned = models.DateTimeField(null=True, blank=True)  # Optional, blank allowed
    deadline_of_return = models.DateTimeField(default=default_deadline)  # Use the function for the default

    STATUSES = [
        ('Taken', 'Taken'),
        ('Returned', 'Returned'),
    ]
    status = models.CharField(max_length=20, choices=STATUSES, default='Taken')

    def __str__(self) -> str:
        return f'{self.book} - {self.status}'