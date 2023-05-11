from django.shortcuts import render
from reviews.models import Category
from .mixins import ListCreateDestroyViewSet


# Create your views here.
class CategoryViewSet(ListCreateDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)
    lookup_field = "slug"
