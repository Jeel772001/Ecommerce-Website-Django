from django.shortcuts import render,redirect
from .models import Cart,Customer,Product,OrderPlaced
from django.views import View
from .forms import CustomerRegistrationForm,CustomerProfileForm
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

class ProductView(View):
 def get(self,request):
  topwears=Product.objects.filter(category='TW')
  bottomwears = Product.objects.filter(category='BW')
  laptops = Product.objects.filter(category='L')
  return render(request,'app/home.html',{'topwear':topwears,'bottomwear':bottomwears,'laptops':laptops})

@method_decorator(login_required,name='dispatch')
class ProductDetailView(View):
   def get(self,request,pk):
     product=Product.objects.get(pk=pk)
     item_already_in_cart = False
     item_already_in_cart = Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
     return render(request,'app/productdetail.html',{'product':product,'item_already_in_cart':item_already_in_cart})

@login_required
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user, product=product).save()
    return redirect('/cart')

def show_cart(request):
    if request.user.is_authenticated:
        user=request.user
        cart=Cart.objects.filter(user=user)
        amount=0.0
        shipping_amount=70.0
        total_amount=0.0
        cart_product=[p for p in Cart.objects.all() if p.user==user]
        if cart_product:
            for p in cart_product:
                tempamount=(p.quantity*p.product.discounted_price)
                amount+=tempamount
                total_amount=amount+shipping_amount
            return render(request, 'app/addtocart.html',{"cart":cart,'totalamount':total_amount,'amount':amount})
        else:
            return render(request,'app/emptycart.html')

def plus_cart(request):
    if request.method=='GET':
        prod_id=request.GET['prod_id']
        c=Cart.objects.get(Q(product=prod_id)&Q(user=request.user))
        c.quantity+=1
        c.save()
        amount = 0.0
        shipping_amount = 70.0
        user=request.user
        cart_product = [p for p in Cart.objects.all() if p.user == user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount
            total_amount = amount + shipping_amount

        data={'quantity':c.quantity,'amount':amount,'totalamount':total_amount}
        return JsonResponse(data)

def minus_cart(request):
    if request.method=='GET':
        prod_id=request.GET['prod_id']
        c=Cart.objects.get(Q(product=prod_id)&Q(user=request.user))
        c.quantity-=1
        c.save()
        amount = 0.0
        shipping_amount = 70.0
        user=request.user
        cart_product = [p for p in Cart.objects.all() if p.user == user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount
            total_amount = amount + shipping_amount

        data={'quantity':c.quantity,'amount':amount,'totalamount':total_amount}
        return JsonResponse(data)

def remove_cart(request):
    if request.method=='GET':
        prod_id=request.GET['prod_id']
        c=Cart.objects.get(Q(product=prod_id)&Q(user=request.user))
        c.delete()

        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        amount=0.0
        shipping_amount=70.0
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount

        data = {'amount': amount, 'totalamount': amount + shipping_amount}
        return JsonResponse(data)



def buy_now(request):
 return render(request, 'app/buynow.html')

def address(request):
 add = Customer.objects.filter(user=request.user)
 return render(request, 'app/address.html', {'address': add, 'active': 'btn-primary'})

@login_required
def orders(request):
 order = OrderPlaced.objects.filter(user=request.user)
 return render(request, 'app/orders.html',{'order':order})

def Topwears(request,data=None):
 if data==None:
   topwears=Product.objects.filter(category='TW')
 elif data=="levis":
   topwears=Product.objects.filter(category='TW').filter(brand=data)
 elif data == "wrangler":
   topwears = Product.objects.filter(category='TW').filter(brand=data)
 elif data == "nike":
   topwears = Product.objects.filter(category='TW').filter(brand=data)
 elif data == "lee":
   topwears = Product.objects.filter(category='TW').filter(brand=data)
 elif data == "above":
   topwears = Product.objects.filter(category='TW').filter(discounted_price__gt=800)
 elif data == "below":
   topwears = Product.objects.filter(category='TW').filter(discounted_price__lt=800)
 return render(request, 'app/topwear.html',{'t':topwears})

def laptop(request,data=None):
 if data==None:
   laptops=Product.objects.filter(category='L')
 elif data=="asus":
   laptops=Product.objects.filter(category='L').filter(brand=data)
 elif data == "acer":
   laptops = Product.objects.filter(category='L').filter(brand=data)
 elif data == "samsung":
   laptops = Product.objects.filter(category='L').filter(brand=data)
 elif data == "hp":
   laptops = Product.objects.filter(category='L').filter(brand=data)
 elif data == "above":
   laptops = Product.objects.filter(category='L').filter(discounted_price__gt=30000)
 elif data == "below":
   laptops = Product.objects.filter(category='L').filter(discounted_price__lt=30000)
 return render(request, 'app/laptop.html',{'l':laptops})


def mobile(request,data=None):
 if data==None:
   mobiles=Product.objects.filter(category='M')
 elif data=="samsung":
   mobiles=Product.objects.filter(category='M').filter(brand=data)
 elif data == "iphone":
   mobiles = Product.objects.filter(category='M').filter(brand=data)
 elif data == "motorola":
   mobiles = Product.objects.filter(category='M').filter(brand=data)
 elif data == "above":
   mobiles = Product.objects.filter(category='M').filter(discounted_price__gt=20000)
 elif data == "below":
   mobiles = Product.objects.filter(category='M').filter(discounted_price__lt=20000)
 return render(request, 'app/mobile.html',{'l':mobiles})

def bottomwear(request,data=None):
 if data==None:
   bwears=Product.objects.filter(category='BW')
 elif data=="levis":
   bwears=Product.objects.filter(category='BW').filter(brand=data)
 elif data == "spykers":
   bwears = Product.objects.filter(category='BW').filter(brand=data)
 elif data == "Rodaster":
   bwears = Product.objects.filter(category='BW').filter(brand=data)
 elif data == "above":
   bwears = Product.objects.filter(category='BW').filter(discounted_price__gt=1200)
 elif data == "below":
   bwears = Product.objects.filter(category='BW').filter(discounted_price__lt=1200)
 return render(request, 'app/bottomwear.html',{'b':bwears})

class CustomerRegistrationView(View):
    def get(self,request):
        form =CustomerRegistrationForm()
        return render(request,'app/customerregistration.html',{'form':form})
    def post(self,request):
        form=CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request,'Congratulations!! Registration Successfully')
            form.save()

        return render(request, 'app/customerregistration.html', {'form': form})

@login_required
def checkout(request):
    user=request.user
    address=Customer.objects.filter(user=user)
    cart_items=Cart.objects.filter(user=user)
    amount=0.0
    shipping_amount=70.0
    totalamount=0.0

    cart_product = [p for p in Cart.objects.all() if p.user == request.user]
    if cart_product:
     for p in cart_product:
        tempamount = (p.quantity * p.product.discounted_price)
        amount += tempamount
     totalamount=amount+shipping_amount
    return render(request, 'app/checkout.html',{'address':address,'totalamount':totalamount,'items':cart_items})

@login_required
def payment_done(request):
    user=request.user
    custid=request.GET.get('custid')
    customer=Customer.objects.get(id=custid)
    cart=Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user,customer=customer,product=c.product,quantity=c.quantity).save()
        c.delete()
    return redirect("orders")


@method_decorator(login_required,name='dispatch')
class ProfileView(View):
    def get(self,request):
        form=CustomerProfileForm()
        return render(request,'app/profile.html',{'form':form,'active':'btn-primary'})

    def post(self,request):
        form=CustomerProfileForm(request.POST)
        if form.is_valid():
            user=request.user
            name=form.cleaned_data['name']
            locality=form.cleaned_data['locality']
            city=form.cleaned_data['city']
            state=form.cleaned_data['state']
            zipcode=form.cleaned_data['zipcode']
            data=Customer(user=user,name=name,locality=locality,city=city,zipcode=zipcode,state=state)
            data.save()
            messages.success(request,'data submitted successfully!!')
        return render(request, 'app/profile.html', {'form': form, 'active': 'btn-primary'})