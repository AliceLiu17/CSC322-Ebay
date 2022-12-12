from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
	#Leave as empty string for base url
	path('', views.store, name="store"),
	path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),
 	path('update_item/', views.updateItem, name="update_item"),
    path('process_order/', views.processOrder, name="process_order"),
    path('complaints/', views.complaints, name='complaints_page'),
    
    path('login/', views.loginPage, name="login"),
	path('register/', views.registerPage, name="register"),
	path('logout/', views.loginPage, name="logout"),
 
 	path('buyer_profile/', views.buyerProfile, name="buyer_profile"),
	path('seller_profile/', views.sellerProfile, name="seller_profile"),
	path('admin_profile/', views.adminProfile, name="admin_profile"),
	path('seller_profile/complaints', views.complaints, name='complaints_page'),
	path('buyer_profile/complaints', views.complaints, name='complaints_page'),
	# path('seller-home/', views.sellerHome, name="seller-home"),
 	# path('admin-home/', views.adminHome, name="admin-home"),

	path('seller_profile/change_password', views.PasswordChangeView.as_view(template_name = 'store/change_password.html'), name='change_password'),
	path('buyer_profile/change_password', views.PasswordChangeView.as_view(template_name = 'store/change_password.html'), name='change_password'),
	#path('^change-password/$', auth_views.password_change, {'post_change_redirect': 'next_page'}, name='password_change'),

 

]