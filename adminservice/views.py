from django.shortcuts import render, redirect, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.hashers import make_password,check_password
from random import *
from django.core.mail import send_mail
from user.models import *
from .models import *
from django.http import HttpResponse
from django.contrib import messages
import hashlib
from django.contrib.sessions.models import Session


def index(request):
    email = request.session['email']
    user = User.objects.filter(email=email)
    if request.session.get('Is_Login'):
        return render(request,'index.html',{'email':email,'user':user})
    return redirect('other_login')


def logout(request):
    del request.session['Is_Login']
    return redirect('other_login')



def signup(request):
    if request.POST:
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        conformpassword=request.POST['conformpassword']

        if password == conformpassword:
            if User.objects.filter(email=email).exists():
                messages.error(request,'Email is Alredy Exists! Please Login..')
            else:
                obj = User(username=username,email=email,password=password)
                obj.save()
                return redirect('other_login')
        else:
            messages.error(request,'Password And Conform Password Should Be Same.!')
    return render(request,'signup.html')

def other_login(request):
    if request.session.get('Is_Login'):
        return redirect('index')
    if request.POST:
        email = request.POST['email']
        password = request.POST['password']
        is_exist = User.objects.filter(email=email)
        if is_exist:
            Userr = User.objects.get(email=email)
            print(check_password(password, Userr.password))

        id = User.objects.filter(email=email,password=password).values_list('id')

        if id:
            request.session['Is_Login'] = True
            request.session['id'] = id[0][0]
            request.session['email'] = email

            return redirect('index')

        else:
            messages.error(request,'Email and Password Is Incorrect.!')
    return render(request,'other-login.html')



def getmail(request):
    if request.POST:
        email = request.POST['email']
        id =User.objects.filter(email=email).values_list('id')
        if id:
            return redirect('forgotpass/'+str(id[0][0]))
        else:
            messages.error(request,'Email Is Incorrect!')
    return render(request,'getemail.html')


def forgotpass(request,id):
    print('get id :',id)
    if request.POST:
        newpassword = request.POST['newpassword']
        conformpassword = request.POST['conformpassword']
        if newpassword == conformpassword:
            print('Equal :',id,newpassword)
            User.objects.filter(id=id).update(password=newpassword)
            return redirect('other_login')
        else:
            messages.error(request,'Password And ConformPassword Should Be Same!')

    return render(request,'forgotpassword.html',{'id':id})


def admin_show(request, id):
    # email = request.session['email']
    user = User.objects.filter(id=id)
    return render(request, 'admin_show_profile.html', {'user': user})


def admin_edit_profile(request, id):
    user = User.objects.filter(id=id)
    return render(request, 'admin_edit_profile.html', {'user': user})


def admin_update_profile(request,id):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        contact = request.POST['contact']
        speciality = request.POST['speciality']

        User.objects.filter(id=id).update(name=name, email=email, contact=contact, speciality=speciality)
        messages.success(request,"Profile updated Successfully")

        return redirect('admin_home')


def chnage_password(request):
    id = request.session.get('user_id')
    print(id)
    if request.method == 'POST':
        pw = request.POST['password']
        pwd = hashlib.md5(pw.encode())
        password = pwd.hexdigest()

        cpw = request.POST['conf_password']
        cpwd = hashlib.md5(cpw.encode())
        conf_password = cpwd.hexdigest()

        if password == conf_password:
            User.objects.filter(id=id).update(password=password)
            messages.success(request,"Password Updated successfully")
            return redirect('index')
        else:
            messages.error(request, "Password and confirm password should be same")

    return render(request, 'change_password.html')



def forgotpass(request):
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

            return render(request, 'admin_otp.html', {'otp':otp, 'email':email})
        else:
            msg1 = "Email Is Not Registed"
            return render(request, 'forgotpass.html', {'email': email, 'msg':msg1})
    else:
        print("error")
        return render(request, 'forgotpass.html')

def new_password(request):
    if request.method == "POST":
        pw = request.POST['password']
        pwd = hashlib.md5(pw.encode())
        password = pwd.hexdigest()
        email = request.session['email']
        # print(email)
        user = User.objects.get(email=email)
        user.password = password
        user.save()
        msg = "Your Password Has Been Changed"
        return redirect('index')
    else:
        return render(request, 'new_password.html')

def admin_otp(request):
    if request.method == "POST":
        otp = request.POST['otp']
        cotp = request.POST['cotp']
        email = request.POST['email']
        print(email)
        if otp == cotp:
            return render(request, 'new_password.html',{'email':email})
        else:
            msg = "Incorrect OTP"
            return render(request, 'admin_otp.html', {'msg':msg, 'otp':otp})
    else:
        return render(request, 'admin_otp.html')





def category(request):
    if request.POST:
        name = request.POST['name']
        obj = Category(name=name)
        obj.save()

    msg = 'Category Name Fatch Successfully!'
    return render(request,'category.html', {'msg':msg})


def allcategory(request):
    form = Category.objects.all
    return render(request, 'allcategory.html',{'form':form})


def categoryedit(request,id):
    form = Category.objects.get(id=id)
    return render(request,'categoryedit.html',{'form':form})


def updatecategory(request,id):
    if request.POST:
        name = request.POST['name']
        form = Category.objects.filter(id=id).update(name=name)
    return redirect('allcategory')


def deletecategory(request,id):
    form = Category.objects.get(id=id)
    form.delete()
    return redirect('allcategory')


def subcategory(request):
    cat = Category.objects.all
    if request.POST:
        subName = request.POST['subName']
        catid = request.POST['catid']
        obj = Subcategory(subName=subName)

        obj.catid_id = catid
        obj.save()
    msg = 'SubCategory Name Fatch Successfully!'
    return render(request,'subcategory.html',{'cat':cat ,'msg':msg})


def allsubcategory(request):
    form = Subcategory.objects.all
    return render(request, 'allsubcategory.html',{'form':form})


def subcategoryedit(request,id):
    cat = Category.objects.all
    form = Subcategory.objects.get(id=id)
    return render(request,'subcategoryedit.html',{'cat': cat,'form': form})



def updatesubcategory(request,id):
    cat = request.POST.get('catid')
    if request.POST:
        subName = request.POST['subName']
        form = Subcategory.objects.filter(id=id).update(subName=subName)
    return redirect('allsubcategory')


def deletesubcategory(request,id):
    form = Subcategory.objects.get(id=id)
    form.delete()
    return redirect('allsubcategory')


def product(request):
    cat = Category.objects.all
    subcat = Subcategory.objects.all
    if request.POST:
        catid = request.POST['cat']
        subcatid = request.POST['subcat']
        prodName = request.POST['prodName']
        prodDescription = request.POST['prodDescription']
        prod_quantity = request.POST['prod_quantity']
        stock = request.POST['stock']
        prodImg = request.FILES['prodImg']
        prodPrice = request.POST['prodPrice']
        obj = Product(prodName=prodName,
                      prodDescription=prodDescription,
                      prod_quantity=prod_quantity,
                      stock=stock,
                      prodImg=prodImg,
                      prodPrice=prodPrice)
        obj.catid_id =catid
        obj.subcatid_id=subcatid
        obj.save()
    msg = 'Product Data Fatch Successfully'
    return render(request,'product.html',{'cat':cat,'subcat':subcat, 'msg':msg})


def allproduct(request):
    form = Product.objects.all
    return render(request, 'allproduct.html',{'form':form})

def productedit(request,id):
    cat = Category.objects.all
    subcat = Subcategory.objects.all
    form = Product.objects.get(id=id)

    return render(request,'productedit.html',{'cat':cat,'subcat':subcat,'form':form})

def updateproduct(request,id):
    if request.POST:
        prodName = request.POST['prodName']
        prodDescription = request.POST['prodDescription']
        prod_quantity = request.POST['prod_quantity']
        prodImg = request.FILES['prodImg']
        prodPrice = request.POST['prodPrice']
        stock = request.POST['stock']
        catid = request.POST['cat']
        subcatid = request.POST['subcat']
        if Product.objects.filter(prodName=prodName).exists():
            messages.error(request, "Product already exist")
        else:
            form = Product.objects.filter(id=id).update(prodName=prodName,
                                                    prodDescription=prodDescription,
                                                    prod_quantity=prod_quantity,
                                                    prodImg=prodImg,
                                                    prodPrice=prodPrice,
                                                    stock=stock,
                                                    catid=catid,
                                                    subcatid=subcatid)
            return redirect('allproduct')

    return redirect('allproduct')


def deleteprodut(request,id):
    form = Product.objects.get(id=id)
    form.delete()
    return redirect('allproduct')



def offer(request):
    prod = Product.objects.all
    if request.POST:
        prodid = request.POST['prodid']
        offername = request.POST['offername']
        startdate = request.POST['startdate']
        enddate = request.POST['enddate']
        discount_amt = request.POST['discount_amt']
        description = request.POST['description']
        obj = Offer(offername=offername,
                    startdate=startdate,
                    enddate=enddate,
                    discount_amt=discount_amt,
                    description=description)
        obj.prodid_id = prodid
        obj.save()
        messages.success(request, 'OfferData  Fatch Successfully!')
    return render(request, 'offer.html', {'prod': prod})


def alloffer(request):
    form = Offer.objects.all
    return render(request,'alloffer.html',{'form':form})


def offeredit(request,id):
    prod = Product.objects.all
    form = Offer.objects.get(id=id)
    return render(request, 'offeredit.html', {'prod': prod,'form':form})


def updateoffer(request,id):
    if request.POST:
        offername = request.POST['offername']
        startdate = request.POST['startdate']
        enddate = request.POST['enddate']
        discount_amt = request.POST['discount_amt']
        description = request.POST['description']
        prodid = request.POST['prodid']
        if Offer.objects.filter(offername=offername).exists():
            messages.error(request, "Product already exist")
        else:
            form = Offer.objects.filter(id=id).update(offername=offername,
                                                    startdate=startdate,
                                                    enddate=enddate,
                                                    discount_amt=discount_amt,
                                                    description=description,
                                                    prodid=prodid)
            return redirect('alloffer')

    return redirect('alloffer')

def all_order(request):
    order_product = Order.objects.all()
    print('order_product :', order_product)
    return render(request,'all_order.html',{'order_product':order_product})

def user_register_data(request):
    user = User_register.objects.all()
    return render(request,'user_register_data.html',{'user':user})


def user_view(request,id):
    user = Order.objects.get(id=id)
    return render(request,'order_view.html',{'user':user})

def deleteoffer(request,id):
    form = Offer.objects.get(id=id)
    form.delete()
    return redirect('alloffer')

def user_feedback(request):
    user = Contact.objects.all()
    return render(request,'feedback.html',{'user':user})

def product_feedback(request):
    user = User_feedback.objects.all()
    return render(request,'product_feedback.html',{'user':user})


def delete_feedback(request,id):
    user = User_feedback.objects.get(id=id)
    user.delete()
    return redirect('product_feedback')

