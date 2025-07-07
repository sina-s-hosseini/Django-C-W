from django.contrib import admin
from .models import Wallet, Transaction


class WalletAdmin(admin.ModelAdmin):
    list_display = ('user', 'balance')
    search_fields = ('user__email', 'user__username')


class TransactionAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'amount', 'timestamp')
    search_fields = ('sender__email', 'receiver__email')
    list_filter = ('timestamp', )


admin.site.register(Wallet, WalletAdmin)
admin.site.register(Transaction, TransactionAdmin)