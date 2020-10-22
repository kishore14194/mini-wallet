from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from .services import AccountServices, WalletServices, TransactionServices


class Init(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        """
		Description : Customer can create a wallet account using this API
		"""
        customer_id = request.data.get("customer_xid", None)
        if customer_id is not None:
            return Response(AccountServices.createAccount(customer_id))
        else:
            return Response({"status": "failed"})


class Manage_wallet(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """
		Description : Customer can get wallet balance using this API
		"""
        user_id = request.user.id

        return Response(WalletServices.getBalance(user_id))

    def post(self, request):
        """
			Description : Customer can enable his wallet using this API
		"""
        user_id = request.user.id
        return Response(WalletServices.enableWallet(user_id))

    def patch(self, request):
        """
			Description : Customer can disable his account using this API
		"""
        return Response(WalletServices.disableWallet(request))


class Deposit(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        """
			Description : Customer can use this API to deposit virtual money in his wallet
		"""
        try:
            amount = float(request.data.get("amount", None))
        except ValueError as e:
            return {"status": "failed", "message": "Invalid amount"}

        ref_id = request.data.get("reference_id", None)

        return Response(TransactionServices.deposit(amount, ref_id, request))


class Withdraw(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        """
		Description : Customer can use this API to withdraw virtual money from his wallet
		"""

        try:
            amount = float(request.data.get("amount", None))
        except ValueError as e:
            return {"status": "failed", "message": "Invalid amount"}
        ref_id = request.data.get("reference_id", None)

        return Response(TransactionServices.withdraw(amount, ref_id, request))
