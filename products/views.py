from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.views.generic import ListView

from products.models import Basket, Product, ProductCategory

PER_PAGE = 3


class ProductsView(ListView):

    model = Product
    context_object_name = 'products'
    template_name = 'products/products.html'
    paginate_by = 3

    def get_queryset(self):
        """Filtration by category. If category_id is not None, return list
         goods filtered by category"""
        query_set = super().get_queryset()
        category_id = self.kwargs.get('category_id')
        return query_set.filter(category_id=category_id) if category_id \
            else query_set

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['categories'] = ProductCategory.objects.all()
        context['title'] = 'Catalog'
        return context


@login_required(redirect_field_name=None)
def add_basket(request, product_id):
    product = Product.objects.get(id=product_id)
    good_in_basket = Basket.objects.filter(user=request.user, product=product)

    if good_in_basket.exists():
        good = good_in_basket.first()
        good.quantity += 1
        good.save()

    else:
        Basket.objects.create(user=request.user, product=product)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def remove_basket(request, product_id):
    product = Product.objects.get(id=product_id)
    Basket.objects.filter(user=request.user, product=product).delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
