from xml.dom import ValidationErr

from django.shortcuts import get_object_or_404
from rest_framework import filters, generics, status
from rest_framework.decorators import api_view
from rest_framework.filters import OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from ..permissions import IsOwner
from rest_framework.permissions import IsAuthenticatedOrReadOnly

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
    permission_classes = [IsAuthenticatedOrReadOnly, ]
    filter_backends = [filters.SearchFilter,OrderingFilter]
    ordering_fields = ['created_at', 'id']
    search_fields = ['title', 'sub_title', 'text', 'author__first_name', 'author__last_name']
    http_method_names = ['get', 'options', 'head', 'patch', 'post', 'delete']

    def get_serializer_class(self):
        return super().get_serializer_class()

    def get_serializer(self, *args, **kwargs):
        return super().get_serializer(*args, **kwargs)

    def get_object(self):
        pk = self.kwargs.get('pk','')
        post = get_object_or_404(self.get_queryset(), pk=pk)
        self.check_object_permissions(self.request,post)
        return post
    
    def get_permissions(self):
        if self.request.method in ['PATCH','DELETE']:
            return [IsOwner(), ]
        return super().get_permissions()
    
    def list(self, request, *args, **kwargs):
        print(request.user.is_authenticated)
        return super().list(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):

        pk = kwargs.get('pk')
        post = self.get_object()
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
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=request.user)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )

    
