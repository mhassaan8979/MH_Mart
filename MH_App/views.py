from django.shortcuts import redirect, render
from MH_App.models import Product, Categories, Filter_Price, Color, Brand, Contact_us, Order, Order_Item
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from cart.cart import Cart
from django.http import JsonResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import stripe
# This is your test secret API key.
stripe.api_key = settings.STRIPE_SECRET_KEY
YOUR_DOMAIN = 'http://127.0.0.1:8000/'

# Create your views here.
def home(request):
    product = Product.objects.filter(status='Publish')
    context = {'product': product}

    return render(request, 'main/home.html', context)


def product(request):
    product = Product.objects.filter(status='Publish')
    categories = Categories.objects.all()
    filter_price = Filter_Price.objects.all().order_by('price')
    color = Color.objects.all()
    brand = Brand.objects.all()

    CID = request.GET.get('categories')
    FPID = request.GET.get('filter_price')
    CLID = request.GET.get('color')
    BID = request.GET.get('brand')

    ATOZID = request.GET.get('ATOZ')
    ZTOAID = request.GET.get('ZTOA')
    PRICE_LOWTOHIGHID = request.GET.get('PRICE_LOWTOHIGH')
    PRICE_HIGHTOLOWID = request.GET.get('PRICE_HIGHTOLOW')
    NEW_PRODUCTID = request.GET.get('NEW_PRODUCT')
    OLD_PRODUCTID = request.GET.get('OLD_PRODUCT')

    if CID:
        product = Product.objects.filter(categories=CID, status='Publish')
    elif FPID:
        product = Product.objects.filter(filter_price=FPID, status='Publish')
    elif CLID:
        product = Product.objects.filter(color=CLID, status='Publish')
    elif BID:
        product = Product.objects.filter(brand=BID, status='Publish')
    elif ATOZID:
        product = Product.objects.filter(status='Publish').order_by('name')
    elif ZTOAID:
        product = Product.objects.filter(status='Publish').order_by('-name')
    elif PRICE_LOWTOHIGHID:
        product = Product.objects.filter(status='Publish').order_by('price')
    elif PRICE_HIGHTOLOWID:
        product = Product.objects.filter(status='Publish').order_by('-price')
    elif NEW_PRODUCTID:
        product = Product.objects.filter(status='Publish', condition='New').order_by('-id')
    elif OLD_PRODUCTID:
        product = Product.objects.filter(status='Publish', condition='Old').order_by('-id')
    else:
        product = Product.objects.filter(status='Publish')


    context = {
        'product': product,
        'categories': categories,
        'filter_price': filter_price,
        'color': color,
        'brand': brand
        }

    return render(request, 'main/product.html', context)


def search(request):
    query = request.GET.get('query')
    product = Product.objects.filter(name__icontains=query)
    context = {'product': product}

    return render(request, 'main/search.html', context)


def product_details(request, id):
    p = Product.objects.filter(id=id).first()
    context = {'p': p}

    return render(request, 'main/product_details.html', context)


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        contact = Contact_us(
            name=name,
            email=email,
            subject=subject,
            message=message,
        )
        subject = subject
        message = message
        email_from = settings.EMAIL_HOST_USER
        try:
            send_mail(subject, message, email_from, ['mhassaan8979@gmail.com'])
            contact.save()
            return redirect('home')
        except:
            return redirect('contact')

    return render(request, 'main/contact.html')


def to_register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')

        cst = User.objects.create_user(username, email, pass1)
        cst.first_name = first_name
        cst.last_name = last_name
        cst.save()
        return redirect('register')

    return render(request, 'registration/auth.html')


def for_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return redirect('login')

    return render(request, 'registration/auth.html')


def for_logout(request):
    logout(request)

    return redirect('home')


@login_required(login_url="/login/")
def cart_add(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("home")


@login_required(login_url="/login/")
def item_clear(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    return redirect("cart_detail")


@login_required(login_url="/login/")
def item_increment(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


@login_required(login_url="/login/")
def item_decrement(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.decrement(product=product)
    return redirect("cart_detail")


@login_required(login_url="/login/")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")


@login_required(login_url="/login/")
def cart_detail(request):
    return render(request, 'cart/cart_detail.html')


@login_required(login_url="/login/")
def check_out(request):
    if request.method == 'POST':
        charge = stripe.checkout.Session.create(
            line_items=[
            {
                'price': 'price_1NsgOaFN7joeiP0pDtnZSanA',
                'quantity': 1,
            },],
            mode='payment',
            success_url=request.build.absolute.uri(reverse('success')) + '?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=request.build.absolute.uri(reverse('home')),
        )
        context = {
            'session_id': 'session.id',
            'stripe_public_key': settings.STRIPE_PUBLIC_KEY
        }
    return render(request, 'cart/check_out.html', context)


@login_required(login_url="/login/")
def place_order(request):
    if request.method == 'POST':
        uid = request.session.get('_auth_user_id')
        cart = request.session.get('cart')
        user = User.objects.get(id=uid)
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        country = request.POST.get('country')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        postcode = request.POST.get('postcode')
        email = request.POST.get('email')
        amount = request.POST.get('amount')
        order_id = request.POST.get('order_id')

        order = Order (
            user = user,
            firstname = firstname,
            lastname = lastname,
            country = country,
            address = address,
            city = city,
            state = state,
            postcode = postcode,
            email = email,
            amount = amount,
            payment_id = order_id,
        )
        order.save()

        for i in cart:
            a = cart[i]['quantity']
            b = {int(cart[i]['price'])}
            total = a*b

            item = Order_Item(
                order = order,
                product = cart[i]['name'],
                image = cart[i]['image'],
                quantity = cart[i]['quantity'],
                price = cart[i]['price'],
                total = total,
            )
    return render(request, 'cart/place_order.html')


def success(request):
    return render(request, 'cart/thank_you.html')