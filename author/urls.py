from django.urls import path
from rest_framework.routers import SimpleRouter
from .views import api

app_name = 'author'
author_api_routers = SimpleRouter()
author_api_routers.register('api',api.AuthorViewSet,basename='author-api')

urlpatterns = [
    

]

urlpatterns += author_api_routers.urls