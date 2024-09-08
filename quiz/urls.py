from django.urls import path
from quiz.views import QuizListView, QuizDetailView

urlpatterns = [
    path('', QuizListView.as_view(), name='quiz-list'),
    path('<int:pk>/', QuizDetailView.as_view(), name='quiz-detail'),
]