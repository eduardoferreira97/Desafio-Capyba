from django.urls import path
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from .views import api

app_name = 'blog'

post_api_v1_router = SimpleRouter()

post_api_v1_router.register(
    'blog',
    api.PostApiv1ViewSet,
    basename="post-api",
)

urlpatterns = [
    path('blog/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('blog/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('blog/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

urlpatterns += post_api_v1_router.urls
