from rest_framework.urls import path
from .views import AdsView


urlpatterns = [
    path('', AdsView.as_view(), name="banner")
]