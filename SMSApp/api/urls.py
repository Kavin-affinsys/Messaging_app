from django.urls import path

from .views import CustomerAPIView, DetailsView, AccountsView, AccountDetailsView, TransactionsView, TransactionDetailsView


urlpatterns = [
    path("<int:pk>/", DetailsView.as_view()),
    path("", CustomerAPIView.as_view()),
    path("accounts/", AccountsView.as_view()),
    path("accounts/<int:pk>/", AccountDetailsView.as_view()),
    path("transactions/", TransactionsView.as_view()),
    path("transactions/<int:transaction_id>/", TransactionDetailsView.as_view()),
    ]
