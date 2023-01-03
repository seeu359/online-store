from django.urls import path

from orders import views

app_name = 'orders'

urlpatterns = [
    path('create/', views.CreateOrderView.as_view(), name='create_order'),

    path('success/', views.SuccessPaymentView.as_view(),
         name='payment_success'),

    path('cancel/', views.CancelPaymentView.as_view(), name='payment_cancel'),
]
