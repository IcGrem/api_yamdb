from rest_framework import serializers
from .models import Categories, Genre, Title, Review, Comment
from django.db.models import Avg


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Categories

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    #name = serializers.CharField( source="title_name")
    #rating = serializers.IntegerField(source=Review.objects.get())
    genre = GenreSerializer(many=True, read_only=True)
    #print("!!!!")
    #print(serializers.FloatField(source=Review.objects.filter(title=id).aggregate(Avg('score'))[score__avg]))
    rating = serializers.FloatField(source=Review.objects.filter(title=id).aggregate(Avg('score'))[score__avg])
    description = serializers.CharField(allow_blank=True)
    category = serializers.CharField( source="category.name", read_only = True)
    class Meta:
        #depth = 1
        fields = ('name', 'year', 'rating', 'description', 'genre', 'category')
        model = Title


#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    class Meta:
        fields = ('id', 'title', 'text', 'author', 'score', 'pub_date')
        model = Review

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    class Meta:
        fields = ('id', 'author', 'review', 'text', 'created')
        model = Comment