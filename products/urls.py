from django.urls import path

from products.views import ProductsView, add_basket, remove_basket

app_name = 'products'

urlpatterns = [
    path('', ProductsView.as_view(), name='products'),

    path('category/<int:category_id>/', ProductsView.as_view(),
         name='cat_filter'),

    path('page/<int:page>/', ProductsView.as_view(), name='paginator'),
    path('basket/add/<int:product_id>/', add_basket, name='add_basket'),

    path('basket/delete/<int:product_id>/', remove_basket,
         name='remove_basket'),
]
