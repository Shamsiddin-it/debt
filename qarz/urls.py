from django.urls import path
from .views import *


urlpatterns = [
    path('debt_list/', DebtListView.as_view(), name='debt_list'),
    path('debt_list/actives/', ActiveListView.as_view(), name='actives'),
    path('debt_list/paids/', PaidListView.as_view(), name='paids'),
    path('debt/<int:pk>/', DebtDetailView.as_view(), name='debt_detail'),
    path('debt/new/', DebtCreateView.as_view(), name='create_debt'),
    path('', HomeView.as_view(), name='home'),
    path("payment/<int:pk>/", ReturnDebtCreateView.as_view(), name = 'record_payment'),
    path('signup/', register, name = 'signup'),
    path('send_sms/<int:pk>/', send_sms_view, name='send_sms'),
    path('runmigrations/', RunMigrationsView.as_view(), name='run-migrations'),
]
