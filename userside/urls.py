"""userside URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import handler500
from user import views as usersvs
from adminservice import views as adminsvs
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    # path('signup',views.signup,name='signup'),
    path('', usersvs.home, name='home'),
    path('register', usersvs.register, name='register'),
    path('login', usersvs.login, name='login'),
    path('user_logout', usersvs.user_logout, name='user_logout'),
    path('show_profile', usersvs.show_profile, name="show_profile"),
    path('editProfile', usersvs.editProfile, name="editProfile"),
    path('customer_order', usersvs.customer_order, name="customer_order"),
    path('customer_order_detail/<int:id>', usersvs.customer_order_detail, name="customer_order_detail"),
    path('changePassword', usersvs.changePassword, name="changePassword"),
    path('otp', usersvs.otp, name="otp"),
    path('newpassword', usersvs.newpassword, name="newpassword"),
    path('forgotpassword', usersvs.forgotpassword, name="forgotpassword"),
    path('make_payment', usersvs.make_payment, name='make_payment'),
    path('thankpage', usersvs.thankpage, name='thankpage'),
    path('blog', usersvs.blog, name='blog'),
    path('about', usersvs.about, name='about'),
    path('shop', usersvs.shop, name='shop'),
    path('contact', usersvs.contact, name='contact'),
    path('payment', usersvs.payment, name='payment'),
    path('quickview/<int:id>', usersvs.quickview, name='quickview'),
    path('addressdetail', usersvs.addressdetail, name='addressdetail'),
    path('checkout', usersvs.checkout, name='checkout'),
    path('cart', usersvs.cart, name='cart'),
    path('cart/add/<int:id>/', usersvs.cart_add, name='cart_add'),
    path('cart/item_clear/<int:id>/', usersvs.item_clear, name='item_clear'),
    path('cart/item_increment/<int:id>/', usersvs.item_increment, name='item_increment'),
    path('cart/item_decrement/<int:id>/', usersvs.item_decrement, name='item_decrement'),
    path('cart/cart_clear/<int:id>', usersvs.cart_clear, name='cart_clear'),
    path('masks', usersvs.masks, name='masks'),
    path('sanitizer', usersvs.sanitizer, name='sanitizer'),
    path('med_cloth', usersvs.med_cloth, name='med_cloth'),
    path('pulse_oximeter', usersvs.pulse_oximeter, name='pulse_oximeter'),
    path('infrared_thermometer', usersvs.infrared_thermometer, name='infrared_thermometer'),
    path('blood_pressure', usersvs.blood_pressure, name='blood_pressure'),
    path('covid_medicine', usersvs.covid_medicine, name='covid_medicine'),


    # Adminservices Urls...
    # path('admin/', admin.site.urls),


    path('index', adminsvs.index, name='index'),
    path('other_login', adminsvs.other_login, name='other_login'),
    path('signup', adminsvs.signup, name='signup'),
    path('logout', adminsvs.logout, name='logout'),
    path('admin_show/<int:id>', adminsvs.admin_show, name="admin_show"),
    path('admin_show/admin_edit_profile/<int:id>', adminsvs.admin_edit_profile, name="admin_edit_profile"),
    path('admin_show/admin_edit_profile/admin_update_profile/<int:id>', adminsvs.admin_update_profile,
         name="admin_update_profile"),
    path('chnage_password', adminsvs.chnage_password, name="chnage_password"),
    path('forgotpass', adminsvs.forgotpass, name="forgotpass"),
    path('new_password', adminsvs.new_password, name="new_password"),
    path('admin_otp', adminsvs.admin_otp, name="admin_otp"),
    path('category', adminsvs.category, name='category'),
    path('allcategory', adminsvs.allcategory, name='allcategory'),
    path('categoryedit/<int:id>', adminsvs.categoryedit, name='categoryedit'),
    path('updatecategory/<int:id>', adminsvs.updatecategory, name='updatecategory'),
    path('deletecategory/<int:id>', adminsvs.deletecategory, name='deletecategory'),
    path('subcategoory', adminsvs.subcategory, name='subcategory'),
    path('allsubcategory', adminsvs.allsubcategory, name='allsubcategory'),
    path('subcategoryedit/<int:id>', adminsvs.subcategoryedit, name='subcategoryedit'),
    path('updatesubcategory/<int:id>', adminsvs.updatesubcategory, name='updatesubcategory'),
    path('deletesubcategory/<int:id>', adminsvs.deletesubcategory, name='deletesubcategory'),
    path('product', adminsvs.product, name='product'),
    path('allproduct', adminsvs.allproduct, name='allproduct'),
    path('productedit/<int:id>', adminsvs.productedit, name='productedit'),
    path('updateproduct/<int:id>', adminsvs.updateproduct, name='updateproduct'),
    path('deleteprodut/<int:id>', adminsvs.deleteprodut, name='deleteprodut'),
    path('offer', adminsvs.offer, name='offer'),
    path('alloffer', adminsvs.alloffer, name='alloffer'),
    path('offeredit/<int:id>', adminsvs.offeredit, name='offeredit'),
    path('updateffer/<int:id>', adminsvs.updateoffer, name='updateoffer'),
    path('deleteoffer/<int:id>', adminsvs.deleteoffer, name='deleteoffer'),
    path('all_order',adminsvs.all_order,name='all_order'),
    path('user_view/<int:id>',adminsvs.user_view,name='user_view'),
    path('user_feedback',adminsvs.user_feedback,name='user_feedback'),


] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

