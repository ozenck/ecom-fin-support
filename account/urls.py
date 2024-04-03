from django.urls import path
from .views import RegisterView, LoginView, UserView, UsersView, LogoutView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='user-create'),
    path('login/', LoginView.as_view(), name='user-login'),
    path('user/', UserView.as_view(), name='user-get'),
    path('user/', UserView.as_view(), name='user-get'),
    path('users/', UsersView.as_view(), name='all-users-get'),
    path('logout/', LogoutView.as_view(), name='user-logout')
]