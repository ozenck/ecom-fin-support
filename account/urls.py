from django.urls import path
from .views import RegisterView, LoginView, UserView, LogoutView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='user-create'),
    path('login/', LoginView.as_view(), name='user-login'),
    path('user/', UserView.as_view(), name='user-get'),
    path('logout/', LogoutView.as_view(), name='user-logout')
]