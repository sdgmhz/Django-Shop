from django.views.generic import FormView, TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from decimal import Decimal
from django.http import JsonResponse
from django.utils import timezone
from django.shortcuts import redirect

from .permissions import HasCustomerAccessPermission
from .models import UserAddressModel, OrderModel, OrderItemModel, CouponModel
from .forms import CheckOutForm
from cart.models import CartModel
from cart.cart import CartSession
from payment.zarinpal_client import ZarinPalSandbox
from payment.models import PaymentModel


class OrderCheckOutView(LoginRequiredMixin, HasCustomerAccessPermission, FormView):
    template_name = "order/checkout.html"
    form_class = CheckOutForm
    success_url = reverse_lazy("order:completed")

    def get_form_kwargs(self):
        kwargs = super(OrderCheckOutView, self).get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs

    def form_valid(self, form):
        user = self.request.user
        cleaned_data = form.cleaned_data
        address = cleaned_data["address_id"]
        coupon = cleaned_data["coupon"]

        cart = CartModel.objects.get(user=user)
        order = self.create_order(address)

        self.create_order_items(order, cart)
        self.clear_cart(cart)
       
        total_price = order.calculate_total_price()
        self.apply_coupon(coupon, order, user, total_price)
        
        order.save()
        
        return redirect(self.create_payment_url(order))
    
    def create_payment_url(self, order):
        zarin_pal = ZarinPalSandbox()
        response = zarin_pal.payment_request(amount=order.get_price())
        payment_obj = PaymentModel.objects.create(
            authority_id=response.get("data", {}).get("authority"),
            amount=order.get_price(),
        )
        order.payment = payment_obj
        order.save()
        return zarin_pal.generate_payment_url(response.get("data", {}).get("authority"))

    
    def create_order(self, address):
        return OrderModel.objects.create(
            user = self.request.user,
            address = address.address,
            state = address.state,
            city = address.city,
            zip_code = address.zip_code,
        )
    
    def create_order_items(self, order, cart):
        for item in cart.cart_items.all():
            OrderItemModel.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.get_price()
            )

    def clear_cart(self, cart):
        cart.cart_items.all().delete()
        CartSession(self.request.session).clear()

    def apply_coupon(self, coupon, order, user, total_price):
        if coupon:
            # total_price -= round(total_price * Decimal(coupon.discount_percent/100))


            order.coupon = coupon
            coupon.used_by.add(user)
            coupon.save()
            
        order.total_price = total_price


    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["addresses"] = UserAddressModel.objects.filter(user=self.request.user)
        cart = CartModel.objects.get(user=self.request.user)
        total_price = cart.calculate_total_price()
        context["total_price"] = total_price
        context["total_tax"] = round(total_price * 0.09)
        return context
    


class OrderCompletedView(LoginRequiredMixin, HasCustomerAccessPermission, TemplateView):
    template_name = "order/completed.html"


class OrderFailedView(LoginRequiredMixin, HasCustomerAccessPermission, TemplateView):
    template_name = "order/failed.html"
    

class ValidateCouponView(LoginRequiredMixin, HasCustomerAccessPermission, View):

    def post(self, request, *args, **kwargs):
        code = request.POST.get("code")
        user = self.request.user

        status_code = 200
        message = "کد تخفیف با موفقیت اعمال شد"

        total_price = 0
        total_tax = 0

        try:
            coupon = CouponModel.objects.get(code=code)
        except CouponModel.DoesNotExist:
            return JsonResponse({"message": "کد تخفیف وازد شده اشتباه است" }, status=404)
        
        else:
            if coupon.used_by.count() >= coupon.max_limit_usage:
                status_code, message = 403, "محدودیت در تعداد استفاده"
            
            elif coupon.expiration_date and coupon.expiration_date < timezone.now():
                status_code, message = 403, "کد تخفیف منقضی شده است"

            elif user in coupon.used_by.all():
                status_code, message = 403, "این کد تخفیف قبلا توسط شما استفاده شده است"
            else:
                cart = CartModel.objects.get(user=self.request.user)
                total_price = cart.calculate_total_price()
                total_price -= round(total_price * (coupon.discount_percent / 100))
                total_tax = round(total_price * 0.09)

        
        return JsonResponse({"message": message, "total_tax": total_tax, "total_price": total_price }, status=status_code)
 