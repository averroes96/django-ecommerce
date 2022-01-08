from django.shortcuts import render
from django.http import JsonResponse
from .models import *
import json
from datetime import datetime
# Create your views here.

def store(request):

     items = []
     order = {
          "get_total": 0,
          "get_quantity": 0
     }
     cartItems_quantity = order["get_quantity"]

     if request.user.is_authenticated:
          customer = request.user.customer
          order, created = Order.objects.get_or_create(customer=customer, complete=False)
          items = order.orderitem_set.all()
          cartItems_quantity = order.get_quantity
     
     products = Product.objects.all()

     context = {
          "products": products,
          "cartItems_quantity": cartItems_quantity,
     }
     return render(request, 'store/store.html', context)

def cart(request):

     items = []
     order = {
          "get_total": 0,
          "get_quantity": 0
     }
     cartItems_quantity = order["get_quantity"]

     if request.user.is_authenticated:
          customer = request.user.customer
          order, created = Order.objects.get_or_create(customer=customer, complete=False)
          items = order.orderitem_set.all()
          cartItems_quantity = order.get_quantity

     context = {
          "items": items,
          "order": order,
          "cartItems_quantity": cartItems_quantity
     }
     return render(request, 'store/cart.html', context)

def checkout(request):
     items = []
     order = {
          "get_total": 0,
          "get_quantity": 0,
          "shipping": False
     }
     cartItems_quantity = order["get_quantity"]

     if request.user.is_authenticated:
          customer = request.user.customer
          order, created = Order.objects.get_or_create(customer=customer, complete=False)
          items = order.orderitem_set.all()
          cartItems_quantity = order.get_quantity

     context = {
          "items": items,
          "order": order,
          "cartItems_quantity": cartItems_quantity
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

     return JsonResponse("Item was added", safe=False)

def processOrder(request):

     print(f"Data: {request.body}")
     transaction_id = datetime.now().timestamp()
     data = json.loads(request.body)

     if request.user.is_authenticated:
          customer = request.user.customer
          order, created = Order.objects.get_or_create(customer=customer, complete=False)
          total = float(data["userInfo"]["total"])
          order.transaction_id = transaction_id

          if total == float(order.get_total):
               order.complete = True
          order.save()

          if order.shipping:
               ShippingAddress.objects.create(
                    customer=customer,
                    order=order,
                    address=data["shippingInfo"]["address"],
                    city=data["shippingInfo"]["city"],
                    state=data["shippingInfo"]["state"],
                    zipcode=data["shippingInfo"]["zipcode"]
               )
     else:
          print("User is not logged in")
     return JsonResponse("Payment completed", safe=False)