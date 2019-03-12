from django.db import models


class Client(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    name = models.TextField()

    def __str__(self):
        return self.name


class ClientAccount(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    COMMISSION_PERCENT_OF_DEAL = 'percent_of_deal'
    NO_COMMISSION = 'no_commission'

    client = models.ForeignKey('payments.Client', on_delete=models.PROTECT)
    number = models.CharField(max_length=64, unique=True)
    currency = models.ForeignKey('payments.Currency', on_delete=models.PROTECT)
    balance = models.DecimalField(decimal_places=2, max_digits=16)

    commission_type = models.CharField(max_length=64, choices=(
        (COMMISSION_PERCENT_OF_DEAL, COMMISSION_PERCENT_OF_DEAL),
        (NO_COMMISSION, NO_COMMISSION),
    ))
    commission_value = models.DecimalField(decimal_places=2, max_digits=16, null=True, blank=True)

    def __str__(self):
        return self.number


class Currency(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    iso_code = models.CharField(max_length=32, primary_key=True)


class CurrencyConversionRate(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    currency_from = models.ForeignKey('payments.Currency', on_delete=models.PROTECT, related_name='+')
    currency_to = models.ForeignKey('payments.Currency', on_delete=models.PROTECT, related_name='+')
    value = models.DecimalField(decimal_places=6, max_digits=16)

    class Meta:
        unique_together = (
            ('currency_from', 'currency_to')
        )

    @classmethod
    def get_conversion_rate_for(cls, currency_from, currency_to, dt):
        return cls.objects.filter(
            created_at__lte=dt,
            currency_from=currency_from,
            currency_to=currency_to,
        ).order_by('-created_at').last()


class TransferFundsOrder(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    STATUS_PENDING = 'pending'
    STATUS_SUCCESS = 'success'
    STATUS_FAILED = 'failed'

    account_from = models.ForeignKey('payments.ClientAccount', on_delete=models.PROTECT, related_name='+')
    account_to = models.ForeignKey('payments.ClientAccount', on_delete=models.PROTECT, related_name='+')

    amount = models.DecimalField(decimal_places=2, max_digits=16)

    status = models.CharField(max_length=32, choices=(
        (STATUS_PENDING, STATUS_PENDING),
        (STATUS_SUCCESS, STATUS_SUCCESS),
        (STATUS_FAILED, STATUS_FAILED),
    ), default=STATUS_PENDING)


class TransferFundsOrderTransaction(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    order = models.OneToOneField('payments.TransferFundsOrder', on_delete=models.PROTECT)
    conversion_rate = models.ForeignKey('payments.CurrencyConversionRate', null=True, on_delete=models.PROTECT)

    total_charged = models.DecimalField(decimal_places=2, max_digits=16)
    commission_charged = models.DecimalField(decimal_places=2, max_digits=16)
