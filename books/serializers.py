from rest_framework import serializers
from .models import Book, BookRating, TakenBook
from datetime import datetime, timedelta
from django.utils.timezone import now
from users.models import Profile

class GiftedBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['title', 'desc', 'cover', 'release_date', 'genre']  # Omit 'origin' as it will be 'Gifted' by default

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

class BookRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookRating
        fields = '__all__'





class TakenBookSerializer(serializers.ModelSerializer):
    book = BookSerializer()  # Вложенный сериализатор для книги
    username = serializers.CharField(write_only=True)
    
    class Meta:
        model = TakenBook
        fields = ['username', 'book', 'date_taken', 'date_returned', 'deadline_of_return', 'status']
        read_only_fields = ['date_taken', 'deadline_of_return']  # Эти поля только для чтения

    def create(self, validated_data):
        username = validated_data.pop('username')
        book_data = validated_data.pop('book')
        
        # Найти пользователя и книгу
        user = Profile.objects.get(username=username)
        book = Book.objects.get(title=book_data['title'])

        # Создать экземпляр TakenBook
        validated_data['date_taken'] = now()  # Установить date_taken на текущее время
        validated_data['deadline_of_return'] = now() + timedelta(days=10)  # Установить deadline_of_return по умолчанию на 10 дней позже
        taken_book = TakenBook.objects.create(user=user, book=book, **validated_data)

        return taken_book
        
