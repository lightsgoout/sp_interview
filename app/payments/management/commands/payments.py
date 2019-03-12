from django.core.management import BaseCommand

from payments.logic.transfer_execute import execute_transfer_order
from payments.models import TransferFundsOrder, TransferFundsOrderTransaction


class Command(BaseCommand):

    def handle(self, *args, **options):
        # TransferFundsOrderTransaction.objects.all().delete()
        # TransferFundsOrder.objects.all().delete()

        for order in TransferFundsOrder.objects.filter(status=TransferFundsOrder.STATUS_PENDING).select_for_update().order_by('id'):
            execute_transfer_order(order)
