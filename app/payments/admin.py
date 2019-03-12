from django.contrib import admin

# Register your models here.
from payments.models import TransferFundsOrderTransaction, TransferFundsOrder, CurrencyConversionRate, Currency, \
    ClientAccount, Client


class ClientAccountAdmin(admin.ModelAdmin):
    list_display = ['client', 'number', 'currency', 'balance']


admin.site.register(TransferFundsOrderTransaction)
admin.site.register(TransferFundsOrder)
admin.site.register(CurrencyConversionRate)
admin.site.register(Currency)
admin.site.register(ClientAccount, ClientAccountAdmin)
admin.site.register(Client)

