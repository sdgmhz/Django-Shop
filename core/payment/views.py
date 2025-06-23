from django.views.generic import View
from django.urls import reverse_lazy
from django.shortcuts import redirect, get_object_or_404

from .models import PaymentModel, PaymentStatusType
from .zarinpal_client import ZarinPalSandbox
from order.models import OrderModel, OrderStatusType

class PaymentVerifyView(View):
    
    def get(self, request, *args, **kwargs):
        authority_id = request.GET.get("Authority")
        status = request.GET.get("Status")

        payment_obj = get_object_or_404(PaymentModel, authority_id=authority_id)
        order_obj = OrderModel.objects.get(payment = payment_obj)
        zarin_pal = ZarinPalSandbox()
        response = zarin_pal.payment_verify(int(payment_obj.amount), payment_obj.authority_id)

        if response.get("data", {}).get("code") == 100 or response.get("data", {}).get("code") == 101:
            payment_obj.ref_id = response["data"]["ref_id"]
            payment_obj.response_code = response["data"]["code"]
            payment_obj.status = PaymentStatusType.success.value
            payment_obj.response_json = response
            payment_obj.save()
            order_obj.status = OrderStatusType.success.value
            order_obj.save()
            return redirect(reverse_lazy("order:completed"))
        else:
            payment_obj.response_code = response["errors"]["code"]
            payment_obj.status = PaymentStatusType.failed.value
            payment_obj.response_json = response
            payment_obj.save()
            order_obj.status = OrderStatusType.failed.value
            order_obj.save()
            return redirect(reverse_lazy("order:failed"))




