from django.urls import path

from .views import CreateUserView

app_name = 'auth'
urlpatterns = [
    path('cadastro/', CreateUserView.as_view(), name='create_user')
]
