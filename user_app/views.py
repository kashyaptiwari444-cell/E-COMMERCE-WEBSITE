from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Register, Cart, CartItem
from admin_app.models import Category, Product


#============================= Register Page ==========================>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

def register_page(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        address = request.POST.get("address")
        pwd = request.POST.get("pwd")
        photo = request.FILES.get("photo")

        Register.objects.create(
            name=name,
            email=email,
            phone=phone,
            photo=photo,
            address=address,
            pwd=pwd
        )
        messages.success(request, "Registered Successfully")
        return redirect("login")
    return render(request, 'register.html')



#============================= Login Page ==========================>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
def login_page(request):
    if request.method == "POST":
        email = request.POST.get("email")
        pwd = request.POST.get("password")

        try:
            user = Register.objects.get(email=email, pwd=pwd)

            request.session["user_id"] = user.id
            request.session["user_name"] = user.name
            request.session["user_email"] = user.email

            messages.success(request, "Login Successful")
            return redirect("homepage")

        except Register.DoesNotExist:
            messages.error(request, "Invalid Email or Password")

    return render(request, "login.html")

    


def homepage(request):
    categories = Category.objects.all().order_by("-id")
    products = Product.objects.all().order_by("-id")
    
    return render(request, "homepage.html", {
        "categories": categories,
        "products":products
    })

#============================= User Main DashBoard ==========================>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
def user_main_dash(request):
    return render(request, "user_main_dash.html")



#============================= User DashBoard ==========================>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
def user_dash(request):
    return render(request, "user_dash.html")





#============================= Add to cart ==========================>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
def add_to_cart(request, id):

    user_id = request.session.get("user_id")

    if not user_id:
        messages.error(request, "Please login first.")
        return redirect("login")

    user = get_object_or_404(Register, id=user_id)

    product = get_object_or_404(Product, id=id)

    cart, created = Cart.objects.get_or_create(
        user=user,
        defaults={"is_active": True}
    )

    item = CartItem.objects.filter(
        cart=cart,
        product=product
    ).first()

    price = product.discount_price if product.discount_price else product.price

    if item:
        item.quantity += 1
        item.price = price
        item.save()
    else:
        CartItem.objects.create(
            cart=cart,
            product=product,
            quantity=1,
            price=price
        )

    return redirect("cart")




#============================= Cart View ==========================>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
def cart(request):

    user_id = request.session.get("user_id")

    if not user_id:
        messages.error(request, "Please login first.")
        return redirect("login")

    user = get_object_or_404(Register, id=user_id)

    cart = Cart.objects.filter(
        user=user,
        is_active=True
    ).first()

    items = []
    subtotal = 0

    if cart:
        items = cart.items.all()
        subtotal = sum(item.total_price for item in items)

    return render(request, "cart.html", {
        "items": items,
        "subtotal": subtotal
    })
    
    

#============================= Delete Cart Item ==========================>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
def remove_cart_item(request, id):
    if request.method == "POST":
        cart_item = get_object_or_404(CartItem, id=id)
        cart_item.delete()

    return redirect("cart")