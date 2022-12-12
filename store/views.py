from django.shortcuts import render, redirect
from django.http import JsonResponse
import json
import datetime
from .models import * 

from .models import * 
from .forms import OrderForm, CreateUserForm

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
#from .filters import OrderFilter
from django.contrib.auth.views import PasswordChangeView
from store.forms import MyPasswordChangeForm


def store(request):

	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		items = order.orderitem_set.all()
		cartItems = order.get_cart_items
	else:
		#Create empty cart for now for non-logged in user
		items = []
		order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
		cartItems = order['get_cart_items']

	products = Product.objects.all()
	context = {'products':products, 'cartItems':cartItems}
	return render(request, 'store/store.html', context)

def cart(request):

	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		items = order.orderitem_set.all()
		cartItems = order.get_cart_items
	else:
		#Create empty cart for now for non-logged in user
		items = []
		order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
		cartItems = order['get_cart_items']

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'store/cart.html', context)

def checkout(request):
	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		items = order.orderitem_set.all()
		cartItems = order.get_cart_items
	else:
		#Create empty cart for now for non-logged in user
		items = []
		order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
		cartItems = order['get_cart_items']

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'store/checkout.html', context)

def updateItem(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']
	print('Action:', action)
	print('Product:', productId)

	customer = request.user.customer
	product = Product.objects.get(id=productId)
	order, created = Order.objects.get_or_create(customer=customer, complete=False)

	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)

	orderItem.save()

	if orderItem.quantity <= 0:
		orderItem.delete()

	return JsonResponse('Item was added', safe=False)

def processOrder(request):
    #print('Data:', request.body)
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    if request.user.is_authenticated:
            customer = request.user.customer
            order, created = Order.objects.get_or_create(customer=customer, complete=False)
            total = float(data['form']['total'])
            order.transaction_id = transaction_id

            if total == order.get_cart_total:
                order.complete = True
            order.save()
            
            ShippingAddress.objects.create(
                customer=customer,
                order=order,
                address=data['shipping']['address'],
                city=data['shipping']['city'],
                state=data['shipping']['state'],
                zipcode=data['shipping']['zipcode'],
			)
            
            # if order.shipping == True:
            #     ShippingAddress.objects.create(
            #     customer=customer,
            #     order=order,
            #     address=data['shipping']['address'],
            #     city=data['shipping']['city'],
            #     state=data['shipping']['state'],
            #     zipcode=data['shipping']['zipcode'],
			# )
    else:
		    print('User is not logged in')
    return JsonResponse('Payment submitted..', safe=False)



def loginPage(request):

	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')

		# the user can login as long as we approve them as a "customer"
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			#return redirect('store')
			if user.username == 'buyer1':
				return redirect('http://127.0.0.1:8000/buyer_profile/') # CHANGE TO PATH TO BUYER ACCOUNT, i just have holders to make sure it works
			elif user.username == 'seller1':
				return redirect('http://127.0.0.1:8000/seller_profile/')	# CHANGE TO PATH OF SELLER ACCOUNT
			elif user.username == 'admin1':
				return redirect('http://127.0.0.1:8000/admin_profile/') # for admins page 
			elif user.username == 'buyerpractice':
				return redirect('http://127.0.0.1:8000/seller_profile/')	# buyer practice, I meant seller
		else:
			messages.info(request, 'username or password is incorrect')
		

	context = {}
	return render(request, 'store/login.html', context)

def logoutUser(request):
	logout(request)
	return redirect('main')

def registerPage(request):
	form = CreateUserForm()
	if request.method == "POST":
		form = CreateUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			user = form.cleaned_data.get('username')
			messages.success(request, 'account was created for ' + user)
			return redirect('login')
	context = {'form':form}
	return render(request, 'store/register.html', context)


def complaints(request):
	if request.method == "GET":
		return render (request, 'store/complaints.html')


def buyerProfile(request):
	if request.method == "GET":
		return render (request, 'store/buyer_profile.html')

def sellerProfile(request):
	if request.method == "GET":
		return render (request, 'store/seller_profile.html')

def adminProfile(request):
 	if request.method == "GET":
 		return render (request, 'store/admin_profile.html')

class PasswordChangeView(PasswordChangeView):
    form_class = MyPasswordChangeForm
    template_name = "store/change_password.html"
# def storeBuyer(request):

# 	if request.user.is_authenticated:
# 		customer = request.user.customer
# 		order, created = Order.objects.get_or_create(customer=customer, complete=False)
# 		items = order.orderitem_set.all()
# 		cartItems = order.get_cart_items
# 	else:
# 		#Create empty cart for now for non-logged in user
# 		items = []
# 		order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
# 		cartItems = order['get_cart_items']

# 	products = Product.objects.all()
# 	context = {'products':products, 'cartItems':cartItems}
# 	return render(request, 'store/store-buyer.html', context)
