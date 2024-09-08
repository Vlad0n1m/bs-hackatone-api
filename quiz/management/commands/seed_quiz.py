from django.core.management.base import BaseCommand
from django.core.files import File
from faker import Faker
import os
from quiz.models import Quiz

class Command(BaseCommand):
    help = 'Seed the database with initial quiz data'

    def handle(self, *args, **kwargs):
        fake = Faker()

        def create_quizzes(n):
            for _ in range(n):
                quiz = Quiz.objects.create(
                    link=fake.url(),
                    title=fake.sentence(nb_words=5),
                    description=fake.text(),
                    cover_image=File(open('covers/quiz-cover.png', 'rb'), name='quiz-cover.png')
                )
                self.stdout.write(self.style.SUCCESS(f'Created quiz: {quiz.title}'))

        if not os.path.isfile('covers/quiz-cover.png'):
            self.stdout.write(self.style.ERROR('Default cover image file not found. Please ensure that quiz_covers/default_cover.png exists.'))
        else:
            Quiz.objects.all().delete()
            create_quizzes(30)
            self.stdout.write(self.style.SUCCESS('Database seeding for quizzes completed.'))