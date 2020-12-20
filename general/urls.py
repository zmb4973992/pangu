from django.urls import path
from general import views

urlpatterns = [
    path('detail/<short_order_number>/', views.Order.as_view(), name='detail'),
    path('add',views.Add.as_view(), name='add'),
]
