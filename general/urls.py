from django.urls import path
from general import views

urlpatterns = [
    path('detail/<short_order_number>/', views.Order.as_view(), name='detail'),
    path('add', views.AddContact.as_view(), name='add_contact'),
    path('edit/<int:contact_id>/', views.EditContact.as_view(), name='edit_contact'),
    path('contact', views.SearchContact.as_view(), name='search_contact')
]
