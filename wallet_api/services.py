from django.db import IntegrityError, transaction
from rest_framework.authtoken.models import Token
from .models import Customer, Wallet, Transaction
from datetime import datetime


class AccountServices(object):
    def createAccount(customer_id):
        """
			Description : Customer can create a wallet account using this API
		"""
        try:
            if not Customer.objects.filter(id=customer_id).exists():
                user = Customer.objects.create(id=customer_id)
                user.save()
            else:
                user = Customer.objects.get(id=customer_id)
            if not Wallet.objects.filter(owned_by=user).exists():
                account = Wallet.objects.create(
                    owned_by=user, balance=0.00, status=True, enabled_at=datetime.now()
                )
                account.save()
            token, _ = Token.objects.get_or_create(user=user)
            return {"data": {"token": token.key}, "status": "success"}
        except IntegrityError as e:
            return {"status": "failed"}


class WalletServices(object):
    def getBalance(user_id):
        """
			Description : Customer can get wallet balance using this API
		"""
        walletobj = Wallet.objects.get(owned_by=user_id)
        if walletobj.status:
            return {
                "status": "success",
                "data": {
                    "wallet": {
                        "id": walletobj.id,
                        "owned_by": walletobj.owned_by_id,
                        "status": "enabled" if walletobj.status else "disabled",
                        "enabled_at": walletobj.enabled_at,
                        "balance": walletobj.balance,
                    }
                },
            }
        else:
            return {"status": "failed", "message": "Wallet is inactive"}

    def enableWallet(user_id):
        """
			Description : Customer can enable his wallet using this API
		"""
        walletobj = Wallet.objects.get(owned_by=user_id)

        if not walletobj.status:
            status = walletobj.enable()
            return {
                "status": "success",
                "data": {
                    "wallet": {
                        "id": walletobj.id,
                        "owned_by": walletobj.owned_by_id,
                        "status": "enabled" if walletobj.status else "disabled",
                        "enabled_at": walletobj.enabled_at,
                        "balance": walletobj.balance,
                    }
                },
            }
        else:
            return {"status": "failed", "message": "Wallet alredy active"}

    def disableWallet(request):
        """
			Description : Customer can disable his account using this API
		"""
        is_disabled = request.data.get("is_disabled", None)
        if is_disabled is not None:
            user_id = request.user.id
            walletobj = Wallet.objects.get(owned_by=user_id)
            status = walletobj.disable()
            if not status:
                return {
                    "status": "success",
                    "data": {
                        "wallet": {
                            "id": walletobj.id,
                            "owned_by": walletobj.owned_by_id,
                            "status": "enabled" if walletobj.status else "disabled",
                            "disabled_at": walletobj.disabled_at,
                            "balance": walletobj.balance,
                        }
                    },
                }
        else:
            return {"status": "failed"}


# custom exception class
class InsufficientBalance(Exception):
    pass


class TransactionServices(object):
    def deposit(amount, ref_id, request):
        """
			Description : Customer can use this API to deposit virtual money in his wallet
		"""

        if amount and ref_id:
            user_id = request.user.id
            walletobj = Wallet.objects.get(owned_by=user_id)
            if walletobj.status:
                try:
                    with transaction.atomic():
                        record = Transaction.objects.create(
                            wallet=walletobj,
                            by_id=user_id,
                            transaction_type="CR",
                            reference_id=ref_id,
                            amount=amount,
                            at=datetime.now(),
                        )
                        record.save()
                        walletobj.deposit(amount)
                    return {
                        "status": "success",
                        "data": {
                            "deposit": {
                                "id": record.id,
                                "deposited_by": record.by_id,
                                "status": "success",
                                "deposited_at": record.at,
                                "amount": record.amount,
                                "reference_id": record.reference_id,
                            }
                        },
                    }
                except IntegrityError as e:
                    return {"status": "failed"}
            else:
                return {"status": "failed", "message": "Wallet is inactive"}
        else:
            return {
                "status": "failed",
                "message": "Kindly provide amount and reference_id",
            }

    def withdraw(amount, ref_id, request):
        """
			Description : Customer can use this API to withdraw virtual money from his wallet
		"""

        if amount and ref_id:
            user_id = request.user.id
            walletobj = Wallet.objects.get(owned_by=user_id)
            if walletobj.status:
                try:
                    with transaction.atomic():
                        record = Transaction.objects.create(
                            wallet=walletobj,
                            by_id=user_id,
                            transaction_type="DR",
                            reference_id=ref_id,
                            amount=amount,
                            at=datetime.now(),
                        )
                        record.save()
                        withdraw_status = walletobj.withdraw(amount)

                        if not withdraw_status:
                            raise InsufficientBalance("Not enough fund in your wallet")
                    return {
                        "status": "success",
                        "data": {
                            "withdrawal": {
                                "id": record.id,
                                "withdrawn_by": record.by_id,
                                "status": "success",
                                "withdrawn_at": record.at,
                                "amount": record.amount,
                                "reference_id": record.reference_id,
                            }
                        },
                    }
                except InsufficientBalance:
                    return {"status": "failed", "message": "Insufficient balance"}
                except IntegrityError as e:
                    return {"status": "failed"}

            else:
                return {"status": "failed", "message": "Wallet is inactive"}
        else:
            return {
                "status": "failed",
                "message": "Kindly provide amount and reference_id",
            }
