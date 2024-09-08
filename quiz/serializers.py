from rest_framework import serializers
from quiz.models import Quiz

class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = ['id', 'link', 'title', 'description', 'cover_image']