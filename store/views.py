from django.shortcuts import render
from .models import Product,OrderItem,Order,ShippingAddress,Customer
from django.http import JsonResponse
import json
import datetime
from .utils import cookieCart

# Create your views here.

def store(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order,created = Order.objects.get_or_create(customer=customer)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        cookieData = cookieCart(request)
        cartItems = cookieData['cart_items']
        items = cookieData['items']

    products = Product.objects.all()
    context = {'products':products,'cart_items':cartItems}

    return render(request,'store/store.html',context)

def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order,created = Order.objects.get_or_create(customer=customer)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        cookieData = cookieCart(request)
        cartItems = cookieData['cart_items']
        items = cookieData['items']
        order = cookieData['order']

    context = {'items':items,'order':order,'cart_items':cartItems}
    return render(request,'store/cart.html',context)

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order,created = Order.objects.get_or_create(customer=customer)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        cookieData = cookieCart(request)
        cartItems = cookieData['cart_items']
        items = cookieData['items']
        order = cookieData['order']

    context = {'items':items,'order':order,'cart_items':cartItems}
    return render(request,'store/checkout.html',context)    

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order,created = Order.objects.get_or_create(customer=customer,complete=False)
    orderitem,created = OrderItem.objects.get_or_create(order=order,product=product)

    if action == 'add':
        orderitem.quantity = orderitem.quantity + 1
    elif action == 'remove':
        orderitem.quantity = orderitem.quantity - 1

    orderitem.save()

    if orderitem.quantity <=0:
        orderitem.delete()  

    print('ProductId:',productId)
    print('Action:',action)

    return JsonResponse('Item was added',safe=False)   

def process_order(request):
    data = json.loads(request.body)
    transaction_id = datetime.datetime.now().timestamp()

    if request.user.is_authenticated:
        customer = request.user.customer
        order,created = Order.objects.get_or_create(customer=customer,complete=False)

    else:
        print('User is not logged in') 

        print('Cookies:',request.COOKIES)
        name = data['userForm']['name']
        email = data['userForm']['email']

        cookieData = cookieCart(request)
        items = cookieData['items']

        customer,created = Customer.objects.get_or_create(
            email=email
        )
        customer.name = name
        customer.save()

        order = Order.objects.create(
            customer = customer,
            complete = False
        )   

        for item in items:
            product = Product.objects.get(id=item['product']['id'])

            orderItem = OrderItem.objects.create(
                product=product,
                order=order,
                quantity=item['quantity']
            )

    total = float(data['userForm']['total'])
    order.transaction_id = transaction_id

    if total == float(order.get_cart_total):
        order.complete = True

    order.save()

    if order.shipping == True:
        ShippingAddress.objects.create(
            customer = customer,
            order = order,
            address = data['shipping']['address'],
            city = data['shipping']['city'],
            state = data['shipping']['state'],
            zipcode = data['shipping']['zipcode']
        )
    if order.complete == True:
        order.delete()
    return JsonResponse('Order in process!',safe=False)    