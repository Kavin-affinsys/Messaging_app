from django.urls import path

from .views import CustomerView

urlpatterns = [
    path('', CustomerView.as_view(), name="home")
]
