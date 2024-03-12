from django.urls import path
from .views import *

urlpatterns = [
    path("say_hello/", say_hello),
    path("profile/", get_profile),
    path("filter_queries/<int:id>/", filter_queries),
    path("queries/", QueryView.as_view(), name='query-view'),
    path("users/signup/", signup),
    path("users/login", login),    
    path('users/forgot_password/', ForgotPasswordAPIView.as_view()),
    path('users/reset_password/', ResetPasswordAPIView.as_view()),
    path('users/change_password/', ChangePasswordAPIView.as_view()),
    path('users/me/', CurrentUserProfileAPIView.as_view())
]