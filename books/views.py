from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Book, BookRating, TakenBook
from .serializers import BookSerializer, BookRatingSerializer, TakenBookSerializer, GiftedBookSerializer
from rest_framework.permissions import IsAuthenticated
from users.models import Profile
from django.utils.timezone import now
from datetime import timedelta

class BookListView(APIView):
    def get(self, request):
        genre = request.GET.get('genre')
        if genre:
            books = Book.objects.filter(genre=genre)
        else:
            books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

class BookDetailView(APIView):
    def get(self, request, id):
        book = get_object_or_404(Book, id=id)
        serializer = BookSerializer(book)
        return Response(serializer.data)

class BookRatingListView(APIView):
    def get(self, request):
        ratings = BookRating.objects.all()
        serializer = BookRatingSerializer(ratings, many=True)
        return Response(serializer.data)

class BookRatingCreateView(APIView):
    def post(self, request):
        serializer = BookRatingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import TakenBookSerializer

class BorrowBookView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = TakenBookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ReturnBookView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        book_title = request.data.get('book_title')

        try:
            user = Profile.objects.get(username=username)
            book = Book.objects.get(title=book_title)
            taken_book = TakenBook.objects.get(user=user, book=book, status='Taken')
            
            # Update the status and date_returned
            taken_book.status = 'Returned'
            taken_book.date_returned = now()
            taken_book.save()

            return Response({'message': 'Book returned successfully'}, status=status.HTTP_200_OK)

        except (Profile.DoesNotExist, Book.DoesNotExist, TakenBook.DoesNotExist):
            return Response({'error': 'Invalid user or book'}, status=status.HTTP_400_BAD_REQUEST)
        
class GiftedBookCreateView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = GiftedBookSerializer(data=request.data)
        if serializer.is_valid():
            # Set the origin to 'Gifted'
            serializer.save(origin=Book.GIFTED)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ExtendBookDeadlineView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # Get the book's ID or title from the request
        book_title = request.data.get('book_title')

        # Find the TakenBook instance for the current user and book
        try:
            book = Book.objects.get(title=book_title)
            taken_book = TakenBook.objects.get(book=book, user=request.user.profile, status='Taken')
        except TakenBook.DoesNotExist:
            return Response({'error': 'Book not found or not taken by the user'}, status=status.HTTP_404_NOT_FOUND)

        # Extend the deadline by 10 days
        taken_book.deadline_of_return += timedelta(days=10)
        taken_book.save()

        return Response({
            'message': 'Deadline extended by 10 days',
            'new_deadline': taken_book.deadline_of_return
        }, status=status.HTTP_200_OK)
    

from rest_framework import generics




class UserTakenBooksView(generics.ListAPIView):
    serializer_class = TakenBookSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Получаем текущего пользователя и фильтруем записи по пользователю
        user = self.request.user.profile
        return TakenBook.objects.filter(user=user)