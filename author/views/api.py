from rest_framework.viewsets import ModelViewSet
from ..serializers import AuthorSerializer
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework import status
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView



class AuthorViewSet(ModelViewSet,ObtainAuthToken,SocialLoginView):
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticated, ]
    adapter_class = GoogleOAuth2Adapter

    def get_queryset(self):
        User = get_user_model()
        qs = User.objects.filter(username=self.request.user.username)
        return qs
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})

class GoogleLogin(SocialLoginView): # if you want to use Implicit Grant, use this
    adapter_class = GoogleOAuth2Adapter
    

    