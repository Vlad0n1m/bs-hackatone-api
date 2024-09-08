from rest_framework import serializers
from .models import Article, ArticleRating

class ArticleRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleRating
        fields = ['rating']

class ArticleSerializer(serializers.ModelSerializer):
    average_rating = serializers.SerializerMethodField()
    author_username = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = ['id', 'title', 'content', 'date', 'author_username', 'average_rating']

    def get_average_rating(self, obj):
        return obj.get_average_rating()

    def get_author_username(self, obj):
        # Assuming that `author` is a ForeignKey to `Profile`, which has a `user` field that is a ForeignKey to `User`
        return obj.author.user.username