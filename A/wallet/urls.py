from .views import WalletDetailView, SendCurrencyView, BuyCurrencyView
from django.urls import path


app_name = 'wallet'
urlpatterns = [
    path('', WalletDetailView.as_view(), name='wallet'),
    path('send/', SendCurrencyView.as_view(), name='send_currency'),
    path('buy/', BuyCurrencyView.as_view(), name='buy_currency'),
]