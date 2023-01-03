import os
from urllib.parse import urljoin
from loguru import logger

import stripe
from django.conf import settings
from django.shortcuts import reverse

from products.models import Basket


stripe.api_key = os.getenv('STRIPE_SECRET_KEY')


def stripe_checkout_session(user):
    line_items = get_items_from_basket(user)
    checkout_session = stripe.checkout.Session.create(
        line_items=line_items,
        mode='payment',
        success_url=get_payment_url(
            reverse('orders:payment_success')),
        cancel_url=get_payment_url(reverse('orders:payment_cancel'))
    )

    return checkout_session.url


def get_payment_url(path):
    url = urljoin(settings.DOMAIN_NAME, path)
    return url


def fulfill_order(session):
    logger.info(session)
    logger.info(session.metadata.order_id)


def get_items_from_basket(user) -> list:
    user_baskets = Basket.objects.filter(user=user)
    line_items = list()
    for basket in user_baskets:
        line_items.append(
            dict(
                price=basket.product.stripe_product_price_id,
                quantity=basket.quantity,
            ),
        )
    return line_items
