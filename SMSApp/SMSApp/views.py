from django.shortcuts import render
from django.views.generic import ListView

from .models import Customer
from .models import Accounts


class CustomerView(ListView):
    model = Customer
    template_name = "Customer_list.html"
