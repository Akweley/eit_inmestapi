from django.urls import path
from .views import *

urlpatterns = [
    path("say_hello/", say_hello),
    path("profile/", get_profile),
    path("filter_queries/<int:id>/", filter_queries),
     path("queries/", QueryView.as_view(), name='query-view'),
]