from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from store.views import IndexView
from orders.views import order_webhook

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view(), name='main'),
    path('stripe/webhook/', order_webhook, name='order_webhook'),
    path('products/', include('products.urls', namespace='products')),
    path('users/', include('users.urls', namespace='users')),
    path('order/', include('orders.urls', namespace='orders')),
    path('accounts/', include('allauth.urls')),
]


if settings.DEBUG:
    urlpatterns.append(path('__debug__/', include('debug_toolbar.urls')))
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
