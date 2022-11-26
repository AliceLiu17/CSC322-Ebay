from django.db import models
from django import forms
from django.contrib.auth.models import User

# Create your models here.
# first model is customer model which has 3 attributes 
# user: one to one to user model, name, email 
# !!!! must change one to ManyToOneField for now use one to one to test??
# https://docs.djangoproject.com/en/4.1/topics/db/examples/many_to_many/
class Customer(models.Model):
	user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
	name = models.CharField(max_length=200, null=True)
	email = models.CharField(max_length=200)
	#user_type = models.CharField(max_length=80, null=True)

	def __str__(self):
		return self.name


# 3 models to make up an order 
# product model will need name price 
class Product(models.Model):
	name = models.CharField(max_length=200)
	price = models.FloatField()
	# digital = models.BooleanField(default=False,null=True, blank=True)
	image = models.ImageField(null=True, blank=True)

	def __str__(self):
		return self.name

	@property
	def imageURL(self):
		try:
			url = self.image.url
		except:
			url = ''
		return url
 
 # many ot one is customer can have multple orders so we use forigen key 
class Order(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
	date_ordered = models.DateTimeField(auto_now_add=True)
	complete = models.BooleanField(default=False)
	transaction_id = models.CharField(max_length=100, null=True)

	def __str__(self):
		return str(self.id)

	@property
	def get_cart_total(self):
		orderitems = self.orderitem_set.all()
		total = sum([item.get_total for item in orderitems])
		return total 

	@property
	def get_cart_items(self):
		orderitems = self.orderitem_set.all()
		total = sum([item.quantity for item in orderitems])
		return total 
    
    # @property
	# def get_cart_items(self):
	# 	orderitems = self.orderitem_set.all()
	# 	total = sum([item.quantity for item in orderitems])
	# 	return total 
    

    
    

class OrderItem(models.Model):
	product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True) # single order can have multiple order type 
	quantity = models.IntegerField(default=0, null=True, blank=True)
	date_added = models.DateTimeField(auto_now_add=True)

	@property
	def get_total(self):
		total = self.product.price * self.quantity
		return total
 
class ShippingAddress(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True) # attach to customer bc if order delted i wnat hsipping address to customer
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
	address = models.CharField(max_length=200, null=False)
	city = models.CharField(max_length=200, null=False)
	state = models.CharField(max_length=200, null=False)
	zipcode = models.CharField(max_length=200, null=False)
	date_added = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.address