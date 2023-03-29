from xml.dom import ValidationErr

from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from ..models import Post
from ..serializers import PostSerializer


class RecipeAPIv2Pagination(PageNumberPagination):
    page_size = 3


class PostApiv1ViewSet(ModelViewSet):

    queryset = Post.objects.filter()
    serializer_class = PostSerializer
    pagination_class = RecipeAPIv2Pagination

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
