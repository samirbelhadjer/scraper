from django.urls import path
from .views import AboutUsView, ContactView


urlpatterns = [
    path('', AboutUsView),
    path('contact', ContactView.as_view()),
]