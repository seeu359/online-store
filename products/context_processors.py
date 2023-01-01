from products.models import Basket


def basket(request):
    return {
        'basket': Basket.objects.filter(
            user=request.user
        ) if request.user.is_authenticated else list(),
    }
