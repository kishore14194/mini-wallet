from django.urls import path
from .views import *

urlpatterns = [
    # Authetication API's
    path("init", Init.as_view()),
    path("wallet", Manage_wallet.as_view()),
    path("wallet/deposits", Deposit.as_view()),
    path("wallet/withdrawals", Withdraw.as_view()),
]
