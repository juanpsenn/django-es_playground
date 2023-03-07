from rest_framework import generics
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework import serializers
from .models import Article
from django.db.models import Q

class ArticlePagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 1000

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'

class ArticleSearchView(generics.ListAPIView):
    serializer_class = ArticleSerializer
    pagination_class = ArticlePagination

    def get_queryset(self):
        query = self.request.query_params.get('q')
        queryset = Article.objects.all()
        if query:
            # split the query into individual words
            words = query.split()

            # create a dynamic query that filters by each word and field combination
            for word in words:
                queryset = queryset.filter(
                    Q(description__icontains=word) |
                    Q(code__icontains=word) |
                    Q(oem_code__icontains=word) |
                    Q(brand__name__icontains=word) |
                    Q(provider__name__icontains=word)
                )

        return queryset