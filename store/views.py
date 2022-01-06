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
     product_id = data["id"]
     action = data["action"]

     customer = request.user.customer
     product = Product.objects.get(id=product_id)
     order, created = Order.objects.get_or_create(customer=customer, complete=False)
     orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

     if action == "add":
          orderItem.quantity = (orderItem.quantity + 1)
     elif action == "remove":
          orderItem.quantity = (orderItem.quantity - 1)

     orderItem.save()

     if(orderItem.quantity <= 0):
          orderItem.delete()

     print(f"ID = {product_id}")
     print(f"action = {action}")
     return JsonResponse("Item was added", safe=False)