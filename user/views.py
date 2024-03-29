import uuid
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render,redirect, HttpResponse
from django.urls import reverse
import razorpay

from .models import *
from adminservice.models import *
from django.contrib import messages
from datetime import datetime
import os
import hashlib
import smtplib
from random import *
from django.contrib.sessions.models import Session
pass

def home(request):
    product = Product.objects.filter(subcatid='5')
    product1 = Product.objects.filter(subcatid='6')
    product2 = Product.objects.filter(subcatid='7')
    product3  = Product.objects.filter(subcatid='8')
    if request.session.has_key('is_login'):
        return render(request,'home.html',{'product':product,'product1':product1,'product2':product2,'product3':product3})
    return redirect('login')


def register(request):
    if request.POST:
        name = request.POST['Name']
        email = request.POST['Email']
        Contact = request.POST['Contact']
        pw = request.POST['Password']
        pwd = hashlib.md5(pw.encode())
        password = pwd.hexdigest()

        cpw = request.POST['Confirm_Password']
        cpwd = hashlib.md5(cpw.encode())
        confirmpassword = cpwd.hexdigest()

        if User_register.objects.filter(email=email).exists():
            msg = 'Email Address Is Already Register !!!'
            return render(request,'home.html',{'msg':msg})
        else:
            obj = User_register(username=name, email=email, user_contact=Contact, password=password)
            obj.save()

            return redirect('home')

def login(request):
    if request.session.has_key('is_login'):
        return redirect('home')
    if request.POST:
        email = request.POST['Email']
        pw = request.POST['Password']
        pwd = hashlib.md5(pw.encode())
        password = pwd.hexdigest()

        count = User_register.objects.filter(email=email, password=password).count()
        if count > 0:
            request.session['is_login'] = True
            request.session['email'] = email
            request.session['user_id'] = User_register.objects.values('id').filter(email=email,password=password)[0]['id']
            #id = request.session['user_id']
            #print(id)
            # user_id = request.session.get('user_id')
            # print(user_id)


            return redirect('home')
        else:
            msg = 'Email or Password Are Incorrect !!!'
            return render(request, 'home.html', {'msg': msg})

    return render(request, 'home.html')


def user_logout(request):
    del request.session['is_login']
    return redirect('login')


def show_profile(request):
    id=request.session.get('user_id')
    user = User_register.objects.filter(id=id)
    print("user id ",id)
    return render(request, 'show_profile.html',{'user':user})


def editProfile(request):
    id=request.session.get('user_id')
    user = User_register.objects.get(id=id)
    return render(request,'editProfile.html',{'user':user})


def updateProfile(request):
    id = request.session.get('user_id')
    if request.method == 'POST':
        name = request.POST['Name']
        email = request.POST['Email']
        Contact = request.POST['Contact']


        if User_register.objects.filter(email=email).exists():
            messages.error(request, "Email Already Exist!! Please login")
        else:
            User_register.objects.filter(id=id).update(username=name, email=email, user_contact=Contact)

        messages.success(request,"Profile updated Successfully")
        return redirect('show_profile')

def changePassword(request):
    id = request.session.get('user_id')

    if request.method == 'POST':
        o = request.POST['olpd']
        ol = hashlib.md5(o.encode())
        old = ol.hexdigest()

        pw = request.POST['Password']
        pwd = hashlib.md5(pw.encode())
        password = pwd.hexdigest()

        cpw = request.POST['Confirm_Password']
        cpwd = hashlib.md5(cpw.encode())
        conf_password = cpwd.hexdigest()

        if User_register.objects.filter(password = old):
            User_register.objects.filter(id=id).update(password=password)
            return redirect('show_profile')

        else:
            msg = "Old Password doesn't Match!"
            return render(request, 'changePassword.html', {'msg': msg})

    return render(request,'changePassword.html')

def forgotpassword(request):
    if request.method == "POST":
        email = request.POST['email']
        is_already_created = User_register.objects.filter(email=email)
        if is_already_created:
            otp = randint(100000, 999999)
            print("OTP IS")
            print(otp)
            subject = 'Otp verification'
            message = f"Your One Time Password Is {otp}"
            from_email = 'ssgadoya@gmail.com'
            to_email = [email]
            send_mail(subject, message, from_email, to_email)
            print("Configuration Mail Send")

            return render(request, 'otp.html', {'otp':otp, 'email':email})
        else:
            msg1 = "Email Is Not Registed"
            return render(request, 'forgotpassword.html', {'email': email, 'msg':msg1})
    else:
        print("error")
        return render(request, 'forgotpassword.html')

def newpassword(request):
    if request.method == "POST":
        pw = request.POST['password']
        pwd = hashlib.md5(pw.encode())
        password = pwd.hexdigest()
        email = request.POST['email']
        #print(email)
        user = User_register.objects.get(email=email)
        user.password = password
        user.save()
        msg1 = "Your Password Has Been Changed"
        return render(request, 'home.html', {'msg':msg1})
    else:
        return render(request, 'newpassword.html')

def otp(request):
    if request.method == "POST":
        otp = request.POST['otp']
        cotp = request.POST['cotp']
        email = request.POST['email']
        print(email)
        if otp == cotp:
            return render(request, 'newpassword.html',{'email':email})
        else:
            msg = "Incorrect OTP"
            return render(request, 'otp.html', {'msg':msg, 'otp':otp})
    else:
        return render(request, 'otp.html')

def cart_add(request, id):
    #id = request.session.get("id")
    #user = User_register.objects.get(id=id)
    #print('customer id:',customer)
    cart = Cart(request)
    product = Product.objects.get(id=id)
    print('product id:',id)
    cart.add(product=product)
    if request.POST:
        name = request.POST['name']
        image = request.POST['image']
        price = request.POST['price']
        quantity = request.POST['quantity']
        prodid = request.POST['product']
        user_id = request.session['user_id']
        print('user_id :',user_id)
        print('quantity :',quantity,id)
        if int(quantity) < 1:
            messages.error(request,'No stock available')
        if Cart.objects.filter(prodid=id, userid=user_id).exists():
            existsing_quantity = Cart.objects.filter(prodid=id,userid=user_id).values_list('quantity')[0][0]
            print('existsing_quantity:',existsing_quantity)
            existsing_quantity += 1
            print('existsing_quantity +:', existsing_quantity)
            per_pro_price = product.prodPrice
            print('per_pro_price:', per_pro_price)
            total_amt = int(existsing_quantity) * int(per_pro_price)
            print('total_amt:', total_amt)
            Cart.objects.filter(prodid=id, userid=user_id).update(quantity=existsing_quantity,price=total_amt)
            return redirect('cart')

        #request.session['cart'] = dict(id=id, quantity=quantity)
        obj = Cart(name=name,image=image,price=price,quantity=1)
        obj.prodid_id = prodid
        obj.userid_id = user_id
        obj.save()

    return redirect(reverse('home'),{'product':product})


def item_clear(request, id):
    cart = Cart.objects.get(id=id)
    print('Remove id:',id)
    cart.remove(cart)
    return redirect("checkout")


def item_increment(request, id):
    quantity = Cart.objects.filter(id=id).values_list('quantity')[0][0]
    print('quantity :',quantity)
    #cart = Cart.objects.get(id=id)
    product_id = Cart.objects.filter(id=id).values_list('prodid_id')[0][0]
    print('increment id:', id, product_id)
    per_pro_price = Product.objects.filter(id=product_id).values_list('prodPrice')[0][0]
    quantity += 1
    print('addition quantity:',int(quantity),int(per_pro_price))
    total_amt = int(quantity) * int(per_pro_price)
    print('total_amt :',total_amt)
    Cart.objects.filter(id=id).update(quantity=quantity,price=total_amt)

    return HttpResponseRedirect(reverse('cart'))


def item_decrement(request, id):
    quantity = Cart.objects.filter(id=id).values_list('quantity')[0][0]
    print('quantity :', quantity)
    # cart = Cart.objects.get(id=id)
    product_id = Cart.objects.filter(id=id).values_list('prodid_id')[0][0]
    print('increment id:', id, product_id)
    per_pro_price = Product.objects.filter(id=product_id).values_list('prodPrice')[0][0]
    quantity -= 1
    print('addition quantity:', int(quantity), int(per_pro_price))
    total_amt = int(quantity) * int(per_pro_price)
    print('total_amt :', total_amt)
    Cart.objects.filter(id=id).update(quantity=quantity, price=total_amt)

    # cart_i_up = int(dictionary['quantity']) + 1
    # request.session['cart']['quantity'] = cart_i_up
    # print('request session :',request.session['cart'])
    # cart_i_down = int(dictionary['prodquantity']) - 1
    # request.session['cart']['prodquantity'] = cart_i_down
    # print('down session :',request.session['cart'])
    return HttpResponseRedirect(reverse('cart'))


def cart_clear(request,id):
    cart = Cart.objects.get(id=id)
    print('id:', id)
    cart.delete()
    return redirect('cart')


"""
def addressdetail(request):
    id = request.session.get('user_id')
    user = Billaddress.objects.get(id=id)
    if request.POST:
        mobile = request.POST['mobile']
        pincode = request.POST['pincode']
        address = request.POST['address']
        name = request.POST['name']
        city = request.POST['city']
        state = request.POST['state']
        user_id = request.session['user_id']
        print(user_id)
        obj = Billaddress(mobile=mobile, pincode=pincode, address=address, name=name, city=city, state=state)
        obj.userid_id = user_id
        obj.save()
        return redirect('make_payment')
    return render(request, 'addressdetail.html', {'user': user})
"""

def make_payment(request):
    id = request.session.get('user_id')
    user = User_register.objects.get(id=id)
    user_id = request.session['user_id']
    print('user_id :', user_id)
    if request.POST:
        name = request.POST['name']
        number = request.POST['number']
        expirationdate = request.POST['expiration-month-and-year']
        print('date :', expirationdate)
        d = datetime.strptime(expirationdate.replace(' / ', '/'), '%m/%y')
        print('date :', d)

        user_id = request.session['user_id']
        obj = Payment(cardName=name, cardNo=number, expirationDate=d)
        obj.userid_id = user_id
        obj.save()
        cart_obj_list = Cart.objects.filter(userid=user_id)
        print('cart id:', id)
        for cart_obj in cart_obj_list:
            order = Order(name=cart_obj.name, price=cart_obj.price, quantity=cart_obj.quantity,
                          prodid=cart_obj.prodid, userid=cart_obj.userid,
                          image=cart_obj.image, Payment_status='success',
                          Payment_mode='debit card',
                          Success_mode='success')
            order.save()
            product_id_new = int(str(cart_obj.prodid).split('(')[1].replace(')', ''))
            print('prodid :', product_id_new)
            existsing_quantity = Product.objects.filter(id=product_id_new).values_list('prod_quantity')[0][0]
            print('existsing_quantity', existsing_quantity)
            new_quantity = int(existsing_quantity) - int(cart_obj.quantity)
            product = Product.objects.filter(id=product_id_new).update(prod_quantity=new_quantity)
            print('cart id :', cart_obj.id)
            remove_cart = Cart.objects.get(id=cart_obj.id)
            remove_cart.delete()

            # print('cart_quantity :',cart_obj.quantity, cart_obj.name)

        return redirect('thankpage')
    return render(request, 'payment.html')

def customer_order(request):
    userid = request.session.get('user_id')
    order_detail = Order.objects.filter(userid=userid)
    return render(request,'customer_order.html',{'order_detail':order_detail})


def customer_order_detail(request,id):
    #userid = request.session.get('user_id')
    order_product = Order.objects.get(id=id)
    print(order_product)
    return render(request,'customer_order_detail.html',{'order_product':order_product})





def contact(request):
    id = request.session.get('user_id')
    user = User_register.objects.get(id=id)
    if request.POST:
        name = request.POST['name']
        email = request.POST['email']
        usermessage = request.POST['message']
        user_id = request.session['user_id']
        print(user_id)
        obj = Contact(name=name,email=email,message=usermessage)
        obj.userid_id = user_id
        obj.save()
    return render(request,'contact.html')


def cart(request):
    cart = Cart.objects.all
    return render(request,'cart.html',{'cart':cart})

def addressdetail(request):
    user_id = request.session['user_id']
    print('user_id :', user_id)
    total = request.POST['total']
    print("---------------t")
    print(total)
    id = request.session.get('user_id')
    user = User_register.objects.get(id=id)
    cart_obj_list = Cart.objects.filter(userid=user_id)
    print('cart id:', id)
    request.session['o_id'] = []
    for cart_obj in cart_obj_list:
        order = Order(name=cart_obj.name, price=cart_obj.price, quantity=cart_obj.quantity,
                      prodid=cart_obj.prodid, userid=cart_obj.userid,
                      image=cart_obj.image, Payment_status='success',
                      Payment_mode='debit card',
                      Success_mode='success')

        order.save()
        request.session['o_id'].append(order.id)
        # request.session['o_date'] = order.Datetime_of_payment

        product_id_new = int(str(cart_obj.prodid).split('(')[1].replace(')', ''))
        print('prodid :', product_id_new)
        existsing_quantity = Product.objects.filter(id=product_id_new).values_list('prod_quantity')[0][0]
        print('existsing_quantity', existsing_quantity)
        new_quantity = int(existsing_quantity) - int(cart_obj.quantity)
        product = Product.objects.filter(id=product_id_new).update(prod_quantity=new_quantity)
        print('cart id :', cart_obj.id)
        remove_cart = Cart.objects.get(id=cart_obj.id)
        remove_cart.delete()

        # print('cart_quantity :',cart_obj.quantity, cart_obj.name)


    return render(request,'addressdetail.html',{'user':user,'total':total,})




def checkout(request):
    print("--------------------------------11")
    id = request.session.get('user_id')
    #user = User_register.objects.get(id=id).values_list('user_id')
    user = User_register.objects.get(id=id)
    print('user id:',user)
    #customer = Customer.objects.get(Customer_ID=user)
    #cid = Cart.objects.all
    cust_cart = Cart.objects.filter(userid=user)
    #cust_cart = Cart.objects.all
    print('cart id:', cust_cart)
    item = 0
    sub_total = 0
    for i in cust_cart:
        item = item + i.quantity
        sub_total = sub_total + i.price
        request.session['t2'] = sub_total
    total = sub_total + 40
    price = i.price
    print("---------------------")
    print(total)
    sub = sub_total
    request.session['t1'] = total
    request.session['t2'] = sub


    client = razorpay.Client(auth=('rzp_test_DoGs52oAjmnP1r', 'qOoywFtCDm8htA6eUBO9cJO8'))
    payment = client.order.create({'amount': total * 100, 'currency': 'INR', 'payment_capture': '1', })

    return render(request, "checkout.html",
                  {'user': user,  'cust_cart': cust_cart, 'item': item, 'sub_total': sub_total,
                   'total': total, 'sub': sub, 'client':client, 'payment':payment,})


def thankpage(request):
    return render(request,'thankpage.html')


def payment(request):
    return render(request,'payment.html')


def quickview(request,id):
    data = Product.objects.get(id=id)
    return render(request,'quickview.html',{'data':data})

def user_feedback(request,id):
    data = Product.objects.get(id=id)
    print('prod id :', data)
    id = request.session.get('user_id')
    user = User_register.objects.get(id=id)
    print('user id:', user)
    if request.POST:
        feedback_message = request.POST['feedback_message']
        user_id = request.session['user_id']
        print(user_id)
        prod_id = request.POST['data']
        print('product id:', prod_id)
        obj = User_feedback(feedback_message=feedback_message)

        obj.userid_id = user_id
        obj.prodid_id = prod_id
        obj.save()
    return render(request,'quickview.html',{'data':data})



def blog(request):
    return render(request,'blog.html')


def about(request):
    return render(request,'about.html')


def shop(request):
    return render(request,'shop.html')



def masks(request):
    product = Product.objects.filter(subcatid='1')
    return render(request,'masks.html',{'product':product})


def sanitizer(request):
    product = Product.objects.filter(subcatid='2')
    return render(request,'sanitizer.html',{'product':product})


def med_cloth(request):
    product = Product.objects.filter(subcatid='3')
    return render(request, 'med_cloth.html', {'product': product})


def pulse_oximeter(request):
    product = Product.objects.filter(subcatid='9')
    return render(request, 'pulse_oximeter.html', {'product': product})


def infrared_thermometer(request):
    product = Product.objects.filter(subcatid='10')
    return render(request, 'infrared_thermometer.html', {'product': product})


def blood_pressure(request):
    product = Product.objects.filter(subcatid='12')
    return render(request, 'blood_pressure.html', {'product': product})


def covid_medicine(request):
    product = Product.objects.filter(subcatid='8')
    return render(request, 'covid_medicine.html', {'product': product})

def Invoice(request):
    user_id = request.session.get('user_id')
    user = User_register.objects.get(id=user_id)
    '''order = Order.objects.filter(id=userid)
    product = Product.objects.all'''
    order_data = Order.objects.filter(userid=user)
    #print('orderid id:', id)
    print("----------")
    order_id = request.session.get('o_id')
    total = request.session.get('t1')
    sub = request.session.get('t2')


    #order = Order.objects.filter(id=order_id)
    print(total)
    print(sub)
    orderdata=[]
    for order_data in order_id:
        order = Order.objects.get(id=order_data)
        orderdata.append(order)
        print('orderdata :',orderdata)

    return render(request, "invoice.html", {'user':user,'order':orderdata,'total':total,'sub':sub})




def View_Invoice(request,id):
    user_id = request.session.get('user_id')
    user = User_register.objects.get(id=user_id)
    order = Order.objects.filter(id=id)



    return render(request,'viewinvoice.html',{'order':order,'user':user,})







