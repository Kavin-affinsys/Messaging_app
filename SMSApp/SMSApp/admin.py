from django.contrib import admin
from .models import Customer, Accounts, TransactionHistory
# Register your models here.

admin.site.register(Customer)
admin.site.register(Accounts)
admin.site.register(TransactionHistory)
