from http import HTTPStatus
import stripe

from django.http import HttpResponse
from django.shortcuts import redirect
from django.conf import settings
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, TemplateView

from orders.forms import CreateOrderForm
from orders.services import stripe_checkout_session, fulfill_order
from products.models import Basket


class SuccessPaymentView(TemplateView):

    template_name = 'orders/success.html'
    extra_context = {
        'title': 'Заказ оплачен успешно',
    }


class CancelPaymentView(TemplateView):

    template_name = 'orders/canceled.html'


class CreateOrderView(CreateView):

    template_name = 'orders/create_order.html'
    extra_context = {
        'title': 'Оформление заказа',
    }
    form_class = CreateOrderForm
    context_object_name = 'order'

    def post(self, request, *args, **kwargs):

        super().post(request, *args, **kwargs)
        redirect_url = stripe_checkout_session(self.request.user)

        return redirect(redirect_url, code=HTTPStatus.SEE_OTHER)

    def form_valid(self, form):

        form.instance.creator = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        baskets = Basket.objects.filter(user=self.request.user)
        context['basket'] = baskets
        return context

    def get_success_url(self):
        user_id = self.request.user.id
        return reverse('users:profile', args=[user_id])


@csrf_exempt
def order_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET,
        )

    except ValueError:
        return HttpResponse(status=HTTPStatus.NOT_FOUND)

    except stripe.error.SignatureVerificationError:
        return HttpResponse(status=HTTPStatus.NOT_FOUND)

    if event['type'] == 'checkout.session.completed':

        session = event['data']['object']

        fulfill_order(session)

    return HttpResponse(status=200)
