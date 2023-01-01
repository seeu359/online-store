from django.contrib.auth.views import LogoutView
from django.urls import path

from users import views

app_name = 'users'

urlpatterns = [
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('register/', views.UserRegistrationView.as_view(), name='register'),
    path('profile/<int:pk>/', views.UserProfileView.as_view(), name='profile'),

    path('verify/<str:email>/<uuid:code>/',
         views.EmailVerificationView.as_view(),
         name='email_ver'),

    path('logout/', LogoutView.as_view(), name='logout'),
]
