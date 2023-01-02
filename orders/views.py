from django.views.generic import CreateView
from django.urls import reverse

from orders.forms import CreateOrderForm
from products.models import Basket


class CreateOrderView(CreateView):

    template_name = 'orders/create_order.html'
    extra_context = {
        'title': 'Оформление заказа',
    }
    form_class = CreateOrderForm
    context_object_name = 'order'

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
