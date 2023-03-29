from django.urls import path
from rest_framework.routers import SimpleRouter

from .views import api

app_name = 'blog'

post_api_v1_router = SimpleRouter()

post_api_v1_router.register(
    'api/v1',
    api.PostApiv1ViewSet,
    basename="post-api",
)

urlpatterns = [

]

urlpatterns += post_api_v1_router.urls
