from django.shortcuts import render
from django.http import JsonResponse
from .models import *
import json
# Create your views here.

def store(request):
     products = Product.objects.all()
     context = {
          "products": products
     }
     return render(request, 'store/store.html', context)

def cart(request):

     items = []
     order = {
          "get_total": 0,
          "get_quantity": 0
     }

     if request.user.is_authenticated:
          customer = request.user.customer
          order, created = Order.objects.get_or_create(customer=customer, complete=False)
          items = order.orderitem_set.all()

     context = {
          "items": items,
          "order": order
     }
     return render(request, 'store/cart.html', context)

def checkout(request):
     items = []
     order = {
          "get_total": 0,
          "get_quantity": 0
     }

     if request.user.is_authenticated:
          customer = request.user.customer
          order, created = Order.objects.get_or_create(customer=customer, complete=False)
          items = order.orderitem_set.all()

     context = {
          "items": items,
          "order": order
     }
     return render(request, 'store/checkout.html', context)

def updateItem(request):
     data = json.loads(request.body)
     id = data["id"]
     action = data["action"]
     print(f"ID = {id}")
     print(f"action = {action}")
     return JsonResponse("Item was added", safe=False)