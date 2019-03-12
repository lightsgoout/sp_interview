from django.db import transaction

from payments.models import ClientAccount, TransferFundsOrderTransaction, CurrencyConversionRate


class TransferException(Exception):
    pass


class NotEnoughFunds(TransferException):
    pass


class CurrencyConversionRateNotFound(TransferException):
    def __init__(self, currency_from, currency_to, dt):
        super().__init__()
        self.currency_from = currency_from
        self.currency_to = currency_to
        self.dt = dt


@transaction.atomic
def _execute_transfer_order(order):
    """
    :type order: payments.models.TransferFundsOrder
    """
    account_from = ClientAccount.objects.select_related().select_for_update().get(pk=order.account_from_id)
    account_to = ClientAccount.objects.select_related().select_for_update().get(pk=order.account_to_id)

    if account_from.currency == account_to.currency:
        conversion_rate = None
        converted_amount = order.amount
    else:
        conversion_rate = CurrencyConversionRate.get_conversion_rate_for(
            currency_from=account_from.currency,
            currency_to=account_to.currency,
            dt=order.created_at,
        )
        if conversion_rate is None:
            raise CurrencyConversionRateNotFound(
                currency_from=account_from.currency,
                currency_to=account_to.currency,
                dt=order.created_at,
            )

        converted_amount = order.amount * conversion_rate.value

    if account_from.commission_type == ClientAccount.NO_COMMISSION:
        commission = 0
    elif account_from.commission_type == ClientAccount.COMMISSION_PERCENT_OF_DEAL:
        commission = converted_amount / 100 * account_from.commission_value
    else:
        raise AssertionError('unknown commission_type: {}'.format(account_from.commission_type))

    total_charged = converted_amount + commission

    TransferFundsOrderTransaction.objects.create(
        order=order,
        conversion_rate=conversion_rate,
        total_charged=total_charged,
        commission_charged=commission,
    )

    account_from.balance -= order.amount
    account_to.balance += converted_amount

    if account_from.balance < 0:
        raise NotEnoughFunds()

    account_from.save(update_fields=('balance',))
    account_to.save(update_fields=('balance',))
    order.status = order.STATUS_SUCCESS
    order.save(update_fields=('status',))


def execute_transfer_order(order):
    try:
        _execute_transfer_order(order)
    except TransferException:
        order.status = order.STATUS_FAILED
        order.save(update_fields=('status',))
