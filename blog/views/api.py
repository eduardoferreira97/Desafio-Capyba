from xml.dom import ValidationErr

from django.shortcuts import get_object_or_404
from rest_framework import filters, generics, status
from rest_framework.decorators import api_view
from rest_framework.filters import OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from ..models import Post
from ..serializers import PostSerializer


class PostApiv1Pagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 10


class PostApiv1ViewSet(ModelViewSet):

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = PostApiv1Pagination
    filter_backends = [filters.SearchFilter,OrderingFilter]
    ordering_fields = ['created_at', 'id']
    search_fields = ['title', 'sub_title', 'text', 'author__first_name', 'author__last_name']

    def partial_update(self, request, *args, **kwargs):

        pk = kwargs.get('pk')
        post = get_object_or_404(self.get_queryset(), pk=pk)
        serializer = PostSerializer(
            instance=post,
            data=request.data,
            many=False,
            context={'request': request},
        )
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationErr as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        print(serializer.errors)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def get_queryset(self):
        qs = super().get_queryset()

        author_id = self.request.query_params.get('author_id', '')

        if author_id != '' and author_id.isnumeric():
            qs = qs.filter(author=author_id)

        return qs
    
