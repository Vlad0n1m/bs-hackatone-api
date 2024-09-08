from django.urls import path
from .views import BookListView, BookDetailView, BookRatingListView, BookRatingCreateView, BorrowBookView, ReturnBookView,GiftedBookCreateView,ExtendBookDeadlineView, UserTakenBooksView

urlpatterns = [
    path('', BookListView.as_view(), name='book-list'),
    path('<int:id>/', BookDetailView.as_view(), name='book-detail'),
    path('ratings/', BookRatingListView.as_view(), name='book-rating-list'),
    path('rate/', BookRatingCreateView.as_view(), name='book-rating-create'),

    path('borrow/', BorrowBookView.as_view(), name='borrow_book'),
    path('return/', ReturnBookView.as_view(), name='return_book'),
    path('gift/', GiftedBookCreateView.as_view(), name='gifted-book-create'),

    path('extend/', ExtendBookDeadlineView.as_view(), name='extend-book-deadline'),
    path('taken-books/', UserTakenBooksView.as_view(), name='user-taken-books'),

    
]