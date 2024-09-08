from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from books.models import Book, BookRating
from faker import Faker
import random
import os
from django.core.files import File
from django.conf import settings
from users.models import Profile

class Command(BaseCommand):
    help = 'Seed the database with initial data'

    def handle(self, *args, **kwargs):
        fake = Faker()

        def create_users(n):
            users = []
            nicknames = set()  # Using a set for faster lookup
            for _ in range(n):
                # Generate unique username
                while True:
                    username = fake.unique.user_name()
                    if username not in nicknames:
                        nicknames.add(username)
                        break

                # Generate user and save to DB
                password = fake.password()
                email = fake.unique.email()
                user = User.objects.create_user(
                    username=username,
                    password=password,
                    email=email
                )
                profile = Profile.objects.get(user=user)
                print(profile)
                users.append(profile)
                self.stdout.write(self.style.SUCCESS(f'Created user: {username}'))
            return users

        def create_books(n):
            genres = [choice[0] for choice in Book.GENRE_CHOICES]
            origins = [choice[0] for choice in Book.ORIGIN_CHOICES]
            
            for _ in range(n):
                try:
                    cover_path = get_cover_path()
                    with open(cover_path, 'rb') as cover_file:
                        book = Book.objects.create(
                            title=fake.sentence(nb_words=3),
                            desc=fake.text(),
                            cover=File(cover_file, name='test.png'),
                            release_date=fake.date_this_decade(),
                            origin=random.choice(origins),
                            genre=random.choice(genres)
                        )
                        self.stdout.write(self.style.SUCCESS(f'Created book: {book.title}'))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Error creating book: {e}'))

        def create_ratings(n):
            books = list(Book.objects.all())
            users = list(Profile.objects.all())
            
            for _ in range(n):
                try:
                    book = random.choice(books)
                    user = random.choice(users)
                    rating = random.randint(0, 5)
                    BookRating.objects.create(
                        book=book,
                        user=user,
                        rating=rating
                    )
                    self.stdout.write(self.style.SUCCESS(f'Created rating: Book: {book.title}, User: {user.username}, Rating: {rating}'))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Error creating rating: {e}'))

        def get_cover_path():
            cover_path = os.path.join(settings.BASE_DIR, 'covers', 'test.png')
            if not os.path.exists(cover_path):
                raise FileNotFoundError(f'Test image file not found at {cover_path}')
            return cover_path

        # Clear existing data and ensure test image file exists
        try:
            get_cover_path()  # This will raise an exception if the file doesn't exist
        except FileNotFoundError as e:
            self.stdout.write(self.style.ERROR(str(e)))
            return

        # Deleting existing records
        Book.objects.all().delete()
        BookRating.objects.all().delete()
        User.objects.exclude(is_superuser=True).delete()  # Don't delete superuser

        # Create new users, books, and ratings
        create_users(10)
        create_books(100)
        create_ratings(300)

        self.stdout.write(self.style.SUCCESS('Database seeding completed successfully.'))