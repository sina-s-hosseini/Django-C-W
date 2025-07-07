from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import UserUpdateForm, ProfileUpdateForm
from wallet.models import Wallet, Transaction
from django.shortcuts import render, redirect
# from django.contrib.auth.models import User
from .forms import CustomUserCreationForm
from django.contrib import messages
from django.db.models import Q, Sum
from .models import UserProfile
from django.views import View


User = get_user_model()


class UserRegisterView(View):
    def get(self, request):
        return render(request, 'users/register.html')

    def post(self, request):
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        # Validate input
        if password1 != password2:
            messages.error(request, "Passwords do not match!")
            return render(request, 'users/register.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken!")
            return render(request, 'users/register.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already in use!")
            return render(request, 'users/register.html')

        # Create user
        user = User.objects.create_user(username=username, email=email, password=password1)
        login(request, user)  # Auto-login after registration
        return redirect('wallet:wallet')  # Redirect to wallet page



class UserLoginView(View):
    def get(self, request):
        return render(request, 'users/login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('wallet:wallet')  # Redirect to wallet after login
        else:
            return render(request, 'users/login.html', {'error': 'Invalid credentials'})



class UserLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('users:login')

    def post(self, request):
        logout(request)
        return redirect('users:login')



class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        # Ensure the user has a profile
        profile, created = UserProfile.objects.get_or_create(user=request.user)

        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=profile)

        return render(request, 'users/profile.html', {
            'user_form': user_form,
            'profile_form': profile_form
        })

    def post(self, request):
        profile, created = UserProfile.objects.get_or_create(user=request.user)

        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('users:profile')

        return render(request, 'users/profile.html', {
            'user_form': user_form,
            'profile_form': profile_form
        })


class DashboardView(LoginRequiredMixin, View):
    def get(self, request):
        wallet = Wallet.objects.get(user=request.user)  # Get user's wallet
        transactions = Transaction.objects.filter(sender=request.user)[:5]  # Last 5 transactions

        sent_total = Transaction.objects.filter(sender=request.user).aggregate(total=Sum('amount'))['total'] or 0
        received_total = Transaction.objects.filter(receiver=request.user).aggregate(total=Sum('amount'))['total'] or 0
        tx_count = Transaction.objects.filter(Q(sender=request.user) | Q(receiver=request.user)).count()
        total_transactions = Transaction.objects.filter(sender=request.user).count() + \
                             Transaction.objects.filter(receiver=request.user).count()

        context = {
            'wallet': wallet,
            'transactions': transactions,
            'sent_total': sent_total,
            'received_total': received_total,
            'tx_count': tx_count,
            'total_transactions': total_transactions,
        }
        return render(request, 'users/dashboard.html', context)





