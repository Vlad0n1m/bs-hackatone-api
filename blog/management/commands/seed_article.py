from django.core.management.base import BaseCommand
from blog.models import Article, ArticleRating
from faker import Faker
import random
from users.models import Profile
class Command(BaseCommand):
    help = 'Seed the database with random articles and ratings'

    def handle(self, *args, **kwargs):
        fake = Faker()
        users = list(Profile.objects.all())


        # Generate random articles
        num_articles = 10  # Number of articles to create
        for _ in range(num_articles):
            article = Article.objects.create(
                title=fake.sentence(nb_words=6),
                content=fake.paragraph(nb_sentences=5),
                date=fake.date_this_year(),
                author = random.choice(users)

            )
            self.stdout.write(self.style.SUCCESS(f'Article "{article.title}" created'))

            # Generate a random rating for each article
            ArticleRating.objects.create(
                article=article,
                user=random.choice(users),
                rating=random.randint(1, 5)  # Rating between 1 and 5
            )
            self.stdout.write(self.style.SUCCESS(f'Rating for "{article.title}" created'))