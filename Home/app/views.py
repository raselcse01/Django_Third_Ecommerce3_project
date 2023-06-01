from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.db.models import Max, Min, Sum

# model import
from app.models import slider, banner, Main_Category, Product, Category, Color, Brand, Coupon_Code
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

from django.contrib import messages
from cart.cart import Cart
# Create your views here.


def Base(request):
    return render(request, 'base.html')

def Home(request):
    Sliders = slider.objects.all().order_by('-id')[0:3]
    Banners = banner.objects.all().order_by('-id')[0:3]
    main_category = Main_Category.objects.all()

    product = Product.objects.filter(section__name = 'Top Deals Of The Day')
    

    context = {
        'Sliders': Sliders,
        'Banners': Banners,
        'main_category': main_category,
        'product': product,
    }
    return render(request, 'Main/home.html',context )

def PRODUCT_DETAILS(request, slug):
    product = Product.objects.filter(slug = slug)
    if product.exists():
        product = Product.objects.get(slug=slug)
    else:
        return redirect('404')

    context = {
        'product': product,
    }

    return render(request, 'product/product_detail.html',context)


def Error404(request):
    return render(request, 'errors/404.html')

def My_Account(request):
    return render(request, 'account/my-account.html')


def Register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        # print(username, email, password)

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username is already exists')
            return redirect('login')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email is already exists')
            return redirect('login')

        user = User(
            username = username,
            email = email,
            
        )
        user.set_password(password)
        user.save()
        return redirect('login')

def Login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Email and Password are Invalid !")
            return redirect('login')
    
        

@login_required(login_url='/accounts/login/')
def Profile(request):
    return render(request, 'profiles/profile.html')


@login_required(login_url='/accounts/login/')
def Profile_Update(request):
    if request.method == "POST":
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_id = request.user.id

        user = User.objects.get(id=user_id)
        user.first_name = first_name
        user.last_name = last_name
        user.username = username
        user.email = email

        if password != None and password != "":
            user.set_password(password)
        user.save()

        messages.success(request, 'Profile Are Successfully Updated')

        return redirect('profile')
        user.save()

def About(request):
    return render(request, 'Main/about.html')

def Contact(request):
    return render(request, 'Main/contact.html')

def PRODUCTS(request):
    category = Category.objects.all()
    product = Product.objects.all()
    color = Color.objects.all()
    brand = Brand.objects.all()

    min_price = Product.objects.all().aggregate(Min('Price'))
    max_price = Product.objects.all().aggregate(Max('Price'))
   
    ColorID = request.GET.get('colorID')
    FilterPrice = request.GET.get('FilterPrice')
    if FilterPrice:
        Int_FilterPrice = int(FilterPrice)
        product = Product.objects.filter(price__lte = Int_FilterPrice)

    elif ColorID:
        product = Product.objects.filter(color = ColorID)

    else:
        product = Product.objects.all()

    context = {
        'category': category,
        'product': product,
        'min_price': min_price,
        'max_price': max_price,
        'FilterPrice':FilterPrice,
        'color':color,
        'brand':brand,
    }
    return render(request, 'product/product.html',context)


def filter_data(request):
    categories = request.GET.getlist('category[]')
    brands = request.GET.getlist('brand[]')
    # product_num = request.GET.getlist('product_num[]')
    brand = request.GET.getlist('brand[]')

    allProducts = Product.objects.all().order_by('-id').distinct()
    if len(categories) > 0:
        allProducts = allProducts.filter(Categories__id__in=categories).distinct()

    
    if len(brands) > 0:
        allProducts = allProducts.filter(Brand__id__in=brands).distinct()

    t = render_to_string('ajax/product.html', {'product': allProducts})

    return JsonResponse({'data': t})



@login_required(login_url="/users/login")
def cart_add(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


@login_required(login_url="/users/login")
def item_clear(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    return redirect("cart_detail")


@login_required(login_url="/users/login")
def item_increment(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


@login_required(login_url="/users/login")
def item_decrement(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.decrement(product=product)
    return redirect("cart_detail")


@login_required(login_url="/users/login")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")


@login_required(login_url="/users/login")
def cart_detail(request):
    cart = request.session.get('cart')
    packing_cost = sum(i['packing_cost'] for i in cart.values() if i)
    tax = sum(i['tax'] for i in cart.values() if i)

    coupne = None
    valid_coupne = None
    invalid_coupne = None
    if request.method == "GET":
        coupon_Code = request.GET.get('coupne_code')
        if coupon_Code:
            try:
                coupne = Coupon_Code.objects.get(code = coupon_Code)
                valid_coupne = "Are Applicable on current order."
            except:
                invalid_coupne = "Invalid Coupne Code."

    context = {
        'packing_cost': packing_cost,
        'tax': tax,
        'coupne': coupne,
        'valid_coupne': valid_coupne,
        'invalid_coupne': invalid_coupne,
    }
    return render(request, 'cart/cart.html', context)

def Checkout(request):
    coupne_discount = None
    if request.method == "POST":
        coupne_discount = request.POST.get('coupne_discount')
    cart = request.session.get('cart')
    packing_cost = sum(i['packing_cost'] for i in cart.values() if i)
    tax = sum(i['tax'] for i in cart.values() if i)

    tax_add_packing_cost = (packing_cost + tax)

    context = {
        'tax_add_packing_cost': tax_add_packing_cost,
        'coupne_discount': coupne_discount,
    }

    return render(request, 'checkout/checkout.html', context)