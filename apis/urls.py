# debts/urls_api.py
from django.urls import path
from .views import (
    DebtListAPIView, 
    ActiveDebtListAPIView, 
    PaidDebtListAPIView, 
    DebtDetailAPIView,
    DebtCreateAPIView,
    ReturnDebtCreateAPIView,
    DebtPaymentsAPIView
)

urlpatterns = [
    path('debts/', DebtListAPIView.as_view(), name='debt-list-api'),
    path('debts/active/', ActiveDebtListAPIView.as_view(), name='active-debt-list-api'),
    path('debts/paid/', PaidDebtListAPIView.as_view(), name='paid-debt-list-api'),
    path('debts/<int:pk>/', DebtDetailAPIView.as_view(), name='debt-detail-api'),
    path('debts/create/', DebtCreateAPIView.as_view(), name='debt-create-api'),
    path('debts/<int:pk>/payments/', ReturnDebtCreateAPIView.as_view(), name='return-debt-create-api'),
    path('debts/<int:pk>/payments-list/', DebtPaymentsAPIView.as_view(), name='debt-payments-list-api'),
]
