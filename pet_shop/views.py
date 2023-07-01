from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from .models import Category, Product, Brand, CartProduct, Cart, OrderedProducts, Order, UserProfile, Promotion
from django.conf import settings
from .forms import FilterForm, EditProductForm, CheckoutForm, LoginForm, CategoryForm, PromotionForm, RegisterForm
import random
from django.shortcuts import redirect, get_object_or_404
from django.utils import timezone


def get_user(request):
    if request.user.is_authenticated:
        user = request.user
        return user
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
        user = User.objects.filter(username=session_key)[:1]
        if user.exists():
            print("User with username: ", session_key, " exists")
            user = user[0]
            return user
        else:
            user = User(username=session_key)
            user.set_password(session_key)
            user.save()
            return user


def home(request):

    print("user is: ", get_user(request))
    categories = Category.objects.all()

    cart_products = CartProduct.objects.filter(user=get_user(request))

    context = {
        'cart_products': cart_products.count(),
        'categories': categories,
        'MEDIA_URL': settings.MEDIA_URL,
    }
    return render(request, 'home.html', context)


def category_view(request, category):
    products = Product.objects.filter(category__name=category)

    today = timezone.now().date()
    for product in products:
        if product.promotion:
            print(product.promotion.calculate_end_date().date())
            print(today)
            if product.promotion.calculate_end_date().date() == today:
                product.promotion.delete()

    form = FilterForm()
    if request.method == "POST":
        form_data = FilterForm(data=request.POST, files=request.FILES)
        if form_data.is_valid():
            price_form = form_data.cleaned_data['price']
            brand_name = form_data.cleaned_data['brand']
            if not brand_name:
                print("Brand is empty")
                products = products.filter(Q(price__lte=price_form) | Q(price=None))
            else:
                brand = Brand.objects.get(name=brand_name)
                products = products.filter(Q(price__lte=price_form) | Q(price=None), Q(brand=brand) | Q(brand=None))
    cart_products = CartProduct.objects.filter(user=get_user(request))
    promotions = Promotion.objects.all()
    context = {
        "promotions": promotions,
        'cart_products': cart_products.count(),
        'products': products,
        'MEDIA_URL': settings.MEDIA_URL,
        'form': form,
        'category': category
    }
    return render(request, f"{category.lower()}.html", context)



# def cats(request):
#     products = Product.objects.filter(category__name="Cats")
#     form = FilterForm()
#     if request.method == "POST":
#         form_data = FilterForm(data=request.POST, files=request.FILES)
#         if form_data.is_valid():
#             price_form = form_data.cleaned_data['price']
#             brand_name = form_data.cleaned_data['brand']
#             if not brand_name:
#                 print("Brand is empty")
#                 products = products.filter(Q(price__lte=price_form) | Q(price=None))
#             else:
#                 brand = Brand.objects.get(name=brand_name)
#                 products = products.filter(Q(price__lte=price_form) | Q(price=None), Q(brand=brand) | Q(brand=None))
#     cart_products = CartProduct.objects.filter(user=get_user(request))
#     context = {
#         'cart_products': cart_products.count(),
#         'products': products,
#         'MEDIA_URL': settings.MEDIA_URL,
#         'form': form,
#     }
#     return render(request, 'cats.html', context)


def edit(request, product_id):
    form = None
    product = get_object_or_404(Product, id=product_id)

    if request.method == "POST":
        form_data = EditProductForm(data=request.POST, files=request.FILES, instance=product)
        if form_data.is_valid():

            product = form_data.save(commit=False)
            product.name = form_data.cleaned_data['name']
            product.desc = form_data.cleaned_data['desc']
            product.keywords = form_data.cleaned_data['keywords']
            product.category = form_data.cleaned_data['category']
            product.brand = form_data.cleaned_data['brand']
            product.price = form_data.cleaned_data['price']
            product.photo = form_data.cleaned_data['photo']
            product.promotion = form_data.cleaned_data['promotion']
            product.has_sizes = form_data.cleaned_data['has_sizes']
            product.has_colors = form_data.cleaned_data['has_colors']

            product.save()

            return redirect('category_view', category=product.category.name)
    else:
        form = EditProductForm(instance=product)

    cart_products = CartProduct.objects.filter(user=get_user(request))
    promotions = Promotion.objects.all()
    context = {
        'promotions': promotions,
        'form': form,
        'MEDIA_URL': settings.MEDIA_URL,
        'cart_products': cart_products.count(),
    }
    return render(request, 'edit.html', context)


def delete(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    return redirect('category_view', category=product.category.name)


def create_product(request):
    form = EditProductForm()
    cart_products = CartProduct.objects.filter(user=get_user(request))
    promotions = Promotion.objects.all()
    context = {'promotions': promotions, 'form': form, 'MEDIA_URL': settings.MEDIA_URL, 'cart_products': cart_products.count()}
    if request.method == "POST":
        form_data = EditProductForm(data=request.POST, files=request.FILES)
        if form_data.is_valid():
            product = form_data.save(commit=False)
            product.name = form_data.cleaned_data['name']
            product.desc = form_data.cleaned_data['desc']
            product.keywords = form_data.cleaned_data['keywords']
            product.category = form_data.cleaned_data['category']
            product.brand = form_data.cleaned_data['brand']
            product.price = form_data.cleaned_data['price']
            product.photo = form_data.cleaned_data['photo']
            product.promotion = form_data.cleaned_data['promotion']
            product.has_sizes = form_data.cleaned_data['has_sizes']
            product.has_colors = form_data.cleaned_data['has_colors']

            product.save()

            today = timezone.now().date()
            if product.promotion:
                if product.promotion.calculate_end_date().date() == today:
                    product.promotion.delete()

            form = EditProductForm()
            text = "Product successfully added."
            cart_products = CartProduct.objects.filter(user=get_user(request))

            context = {'promotions': promotions, 'form': form, 'MEDIA_URL': settings.MEDIA_URL, 'cart_products': cart_products.count(), 'text': text, 'product': product}
    return render(request, 'edit.html', context)


def view(request, product_id):

    product = get_object_or_404(Product, id=product_id)
    today = timezone.now().date()
    if product.promotion:
        if product.promotion.calculate_end_date().date() == today:
            product.promotion.delete()
    cart_products = CartProduct.objects.filter(user=get_user(request))
    promotion = Promotion.objects.all()
    context = {'promotions': promotion, 'product': product, 'MEDIA_URL': settings.MEDIA_URL, 'cart_products': cart_products.count(),}
    return render(request, 'product.html', context)


def add_to_cart(request, product_id):
    user = get_user(request)
    product = get_object_or_404(Product, id=product_id)
    today = timezone.now().date()
    if product.promotion:
        if product.promotion.calculate_end_date().date() == today:
            product.promotion.delete()
    quantity = request.POST.get('quantity', 1)
    size = request.POST.get('size')
    color = request.POST.get('color')

    if size is None:
        size = 'M'

    existing_cart_product = CartProduct.objects.filter(
        user=user,
        product=product,
        size=size,
        color=color
    ).first()

    if existing_cart_product:
        existing_cart_product.quantity += int(quantity)
        existing_cart_product.save()
    else:
        cart_product = CartProduct(user=user, product=product, quantity=quantity, size=size, color=color)
        cart_product.save()

        cart, created = Cart.objects.get_or_create(user=user)
        cart.products.add(cart_product)

    return redirect('category_view', category=product.category.name)


def cart(request):
    user_cart, created = Cart.objects.get_or_create(user=get_user(request))
    products = user_cart.products.all()
    today = timezone.now().date()
    for product in products:
        if product.promotion:
            if product.promotion.calculate_end_date().date() == today:
                product.promotion.delete()
    cart_products = CartProduct.objects.filter(user=get_user(request))
    total = 0.0
    for cart_product in cart_products:
        if cart_product.product.promotion is not None:
            promotion = cart_product.product.price * (cart_product.product.promotion.amount / 100)
            cart_product.product.price = cart_product.product.price - promotion
        cart_product.product.price = cart_product.product.price * int(cart_product.quantity)
        total = total + cart_product.product.price
    total = format(total, '.2f')
    context = {
        'products': products,
        'cart_products': cart_products.count(),
        'MEDIA_URL': settings.MEDIA_URL,
        'total': total,
    }
    return render(request, 'cart.html', context)


def remove_from_cart(request, product_id):
    cart_product = get_object_or_404(CartProduct, id=product_id)
    cart_product.delete()
    return redirect('cart')


def checkout(request):
    cart_products = CartProduct.objects.filter(user=get_user(request))
    user_profile_exists = UserProfile.objects.filter(user=get_user(request)).exists()
    user_info =None
    if user_profile_exists:
        user_info = UserProfile.objects.get(user=get_user(request))

    if request.method == "POST":
        form_data = CheckoutForm(data=request.POST, files=request.FILES)
        if form_data.is_valid():
            order = form_data.save(commit=False)
            order.user = get_user(request)
            order.name = form_data.cleaned_data['name']
            order.surname = form_data.cleaned_data['surname']
            order.email = form_data.cleaned_data['email']
            order.address = form_data.cleaned_data['address']
            order.phone_number = form_data.cleaned_data['phone_number']
            order.postcode = form_data.cleaned_data['postcode']
            order.payment_type = form_data.cleaned_data['payment_type']
            order.remark = form_data.cleaned_data['remark']
            order.number = int(random.random() * 1000000)
            order.save()

            for cart_product in cart_products:
                ordered_product = OrderedProducts(
                    user=cart_product.user,
                    product=cart_product.product,
                    quantity=cart_product.quantity,
                    size=cart_product.size,
                    color=cart_product.color
                )
                ordered_product.save()
                order.cart_products.add(ordered_product)

            order.save()

            user_cart, created = Cart.objects.get_or_create(user=get_user(request))
            user_cart.products.clear()
            cart_products.delete()
            form = CheckoutForm()
            text = "Thank you for you order!"
            user_cart_products  = CartProduct.objects.filter(user=get_user(request))

            context = {
                'order': order,
                'form': form,
                'cart_products': user_cart_products.count(),
                'MEDIA_URL': settings.MEDIA_URL,
                'text': text,
            }
    else:
        form = CheckoutForm(initial={
            'name': user_info.name if user_info else '',
            'surname': user_info.surname if user_info else '',
            'email': user_info.email if user_info else '',
            'address': user_info.address if user_info else '',
            'phone_number': user_info.phone_number if user_info else '',
            'postcode': '',
            'payment_type': '',
            'remark': '',
        })
        context = {
            'form': form,
            'cart_products': cart_products.count(),
            'MEDIA_URL': settings.MEDIA_URL,
        }
    return render(request, 'form.html', context)


def view_orders(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        processed_order = Order.objects.filter(id=order_id)
        processed_order.update(processed=True)


    cart_products = CartProduct.objects.filter(user=get_user(request))
    orders = Order.objects.all()
    context = {
        'orders': orders,
        'cart_products': cart_products.count(),
        'MEDIA_URL': settings.MEDIA_URL,
    }
    return render(request, 'view_orders.html', context)

def search_results(request):
    query = request.GET.get('query', '')
    products = Product.objects.filter(Q(keywords__icontains=query) | Q(name__icontains=query) | Q(category__name__icontains=query))
    today = timezone.now().date()
    for product in products:
        if product.promotion:
            if product.promotion.calculate_end_date().date() == today:
                product.promotion.delete()
    cart_products = CartProduct.objects.filter(user=get_user(request))
    form = FilterForm()
    if request.method == "POST":
        form_data = FilterForm(data=request.POST, files=request.FILES)
        if form_data.is_valid():
            price_form = form_data.cleaned_data['price']
            brand_name = form_data.cleaned_data['brand']
            if not brand_name:
                print("Brand is empty")
                products = products.filter(Q(price__lte=price_form) | Q(price=None))
            else:
                brand = Brand.objects.get(name=brand_name)
                products = products.filter(Q(price__lte=price_form) | Q(price=None), Q(brand=brand) | Q(brand=None))
    promotion = Promotion.objects.all()
    context = {
        'promotions': promotion,
        'cart_products': cart_products.count(),
        'products': products,
        'MEDIA_URL': settings.MEDIA_URL,
        'form': form,
    }
    return render(request, 'view_products.html', context)


def logout_form(request):
    logout(request)
    return redirect("home")


def login_form(request):
    form = LoginForm()
    context = {'form': form}
    if request.method == "POST":
        form_data = LoginForm(data=request.POST, files=request.FILES)
        if form_data.is_valid():
            username = form_data.cleaned_data['your_username']
            password = form_data.cleaned_data['your_password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                print("User exists")
                print(user, request.user)
                return redirect("home")
            else:
                print("User doesn't exist")
                return redirect("login_form")
    return render(request, 'login.html', context)


def add_category(request):
    form = CategoryForm()
    cart_products = CartProduct.objects.filter(user=get_user(request))
    context = {'form': form, 'MEDIA_URL': settings.MEDIA_URL, 'cart_products': cart_products.count()}
    if request.method == "POST":
        form_data = CategoryForm(data=request.POST, files=request.FILES)
        if form_data.is_valid():
            category = form_data.save(commit=False)
            category.name = form_data.cleaned_data['name']
            category.photo = form_data.cleaned_data['photo']

            category.save()
            form = CategoryForm()
            text = "Category successfully added."

            context = {'form': form, 'MEDIA_URL': settings.MEDIA_URL, 'cart_products': cart_products.count(),
                       'text': text}
    return render(request, 'add_category.html', context)


def remove_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    category.delete()
    return redirect('home')

def add_promotion(request, product_id):

    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        amount = request.POST.get('amount')
        duration = int(request.POST.get('duration'))
        product_id = request.POST.get('product_id')
        product = get_object_or_404(Product, id=product_id)
        try:
            promotion = Promotion.objects.get(amount=amount, duration=duration)
        except Promotion.DoesNotExist:
            promotion = Promotion(amount=amount, start_date=timezone.now(), duration=duration)
            promotion.save()

        product.promotion = promotion
        product.save()

    return redirect('category_view', category=product.category.name)


def remove_promotion(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        action = request.POST.get('action')
        promotion_id = request.POST.get('promotion_id')
        promotion = get_object_or_404(Promotion, id=promotion_id)
        if action == 'all':
            promotion.delete()
        else:
            product.promotion = None
            product.save()
    return redirect('category_view', category=product.category.name)


def register(request):
    form = RegisterForm()
    context = {'form': form, 'MEDIA_URL': settings.MEDIA_URL}
    if request.method == "POST":
        form_data = RegisterForm(data=request.POST, files=request.FILES)
        if form_data.is_valid():
            userprofile = form_data.save(commit=False)
            username = request.POST.get('username')
            password = request.POST.get('password')
            email = form_data.cleaned_data['email']
            new_user = User.objects.create_user(username=username, email=email, password=password)
            new_user.save()
            userprofile.user = new_user
            userprofile.name = form_data.cleaned_data['name']
            userprofile.surname = form_data.cleaned_data['surname']
            userprofile.email = form_data.cleaned_data['email']
            userprofile.address = form_data.cleaned_data['address']
            userprofile.phone_number = form_data.cleaned_data['phone_number']

            userprofile.save()

            # username = form_data.cleaned_data['username']
            # password = form_data.cleaned_data['password']
            # email = form_data.cleaned_data['email']
            # user = User.objects.create_user(username=username, password=password, email=email)
            # userprofile = form_data.save(commit=False)
            # userprofile.user = user
            # userprofile.save()

            return redirect('login_form')

    return render(request, 'register.html', context)
