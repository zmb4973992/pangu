from django.contrib import admin

# Register your models here.
from general.models import Contact, Vendor, Order, Guarantee, OrderToGuarantee, UserInformation

admin.site.register([Contact, Vendor, Order, Guarantee, OrderToGuarantee, UserInformation])
