from django_filters import rest_framework as filters
from review.models import Title, Genre
    
class GenreFilter(filters.FilterSet):
    #slug = filters.ModelChoiceFilter(queryset=Genre.objects.all())
    genre_filter = filters.CharFilter(field_name="genre__slug", lookup_expr='exact')
    #print(slug)
    class Meta:
        model = Title
        fields = ['genre_filter']

    # """Filter for books by author"""
    # author = ModelChoiceFilter(queryset=Author.objects.all())

    # class Meta:
    #     model = Book
    #     fields = ['author']