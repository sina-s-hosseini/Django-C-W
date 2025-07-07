from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import Wallet, Transaction
from django.contrib.auth import get_user_model
from django.contrib import messages
from decimal import Decimal

User = get_user_model()


@method_decorator(login_required, name='dispatch')
class WalletDetailView(View):
    def get(self, request):
        wallet, created = Wallet.objects.get_or_create(user=request.user)
        transactions = Transaction.objects.filter(sender=request.user) | Transaction.objects.filter(receiver=request.user)
        return render(request, 'wallet/wallet.html', {'wallet': wallet, 'transactions': transactions})


@method_decorator(login_required, name='dispatch')
class SendCurrencyView(View):
    def get(self, request):
        return render(request, 'wallet/send_currency.html')

    def post(self, request):
        receiver_username = request.POST.get('receiver')
        amount = request.POST.get('amount')

        try:
            amount = Decimal(amount)
            if amount <= 0:
                messages.error(request, "Amount must be greater than zero.")
                return render(request, 'wallet/send_currency.html')

            receiver = User.objects.get(username=receiver_username)
            sender_wallet = Wallet.objects.get(user=request.user)
            receiver_wallet, created = Wallet.objects.get_or_create(user=receiver)

            if sender_wallet.balance >= amount:
                sender_wallet.balance -= amount
                receiver_wallet.balance += amount
                sender_wallet.save()
                receiver_wallet.save()

                Transaction.objects.create(sender=request.user, receiver=receiver, amount=amount)

                messages.success(request, "Transaction successful!")
                return redirect('wallet:wallet')
            else:
                messages.error(request, "Insufficient balance!")
        except User.DoesNotExist:
            messages.error(request, "Receiver not found!")
        except Exception as e:
            messages.error(request, f"Error: {e}")

        return render(request, 'wallet/send_currency.html')


@method_decorator(login_required, name='dispatch')
class BuyCurrencyView(View):
    def get(self, request):
        return render(request, 'wallet/buy_currency.html')

    def post(self, request):
        amount = request.POST.get('amount')

        try:
            amount = Decimal(amount)
            if amount <= 0:
                messages.error(request, "Amount must be greater than zero.")
                return render(request, 'wallet/buy_currency.html')

            wallet, created = Wallet.objects.get_or_create(user=request.user)
            wallet.balance += amount
            wallet.save()

            messages.success(request, f"Successfully bought {amount} ETH!")
            return redirect('wallet:wallet')

        except Exception as e:
            messages.error(request, f"Error: {e}")
            return render(request, 'wallet/buy_currency.html')