from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Register, Cart, CartItem, Order, OrderItem
from admin_app.models import Category, Product
import uuid


#============================= Register Page ==========================>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

def register_page(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        address = request.POST.get("address")
        pwd = request.POST.get("pwd")
        photo = request.FILES.get("photo")
        role = request.POST.get("role")

        Register.objects.create(
            name=name,
            email=email,
            phone=phone,
            photo=photo,
            address=address,
            pwd=pwd,
            role=role
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

    return render(request, "login.html")

    

login_required
def homepage(request):
    categories = Category.objects.all().order_by("-id")
    products = Product.objects.all().order_by("-id")
   
    return render(request, "homepage.html", {
        "categories": categories,
        "products":products,
      
    })

#============================= User Main DashBoard ==========================>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
def user_main_dash(request):
    return render(request, "user_main_dash.html")



#============================= User DashBoard ==========================>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
def user_dash(request):
    return render(request, "user_dash.html")






def view_product(request):
    view_products = get_object_or_404(CartItem, id=id)
    return render(request, "view_product.html", {"view_products":view_products})





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
# ============================= Cart View =============================

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
    discount = 0
    platform_fee = 0
    total = 0

    if cart:

        items = cart.items.all()

        platform_fee = 10

        for item in items:

            # Original Price
            original_price = item.product.price

            # Selling Price
            if item.product.discount_price > 0:
                selling_price = item.product.discount_price
            else:
                selling_price = original_price

            # Item Total
            item.item_total = selling_price * item.quantity

            # Item Discount
            item.item_discount = (
                original_price - selling_price
            ) * item.quantity

            # Discount Percentage
            if original_price > 0 and selling_price < original_price:

                item.discount_percentage = round(
                    (
                        (original_price - selling_price)
                        / original_price
                    ) * 100
                )

            else:
                item.discount_percentage = 0

            # Add to Subtotal
            # subtotal += item.item_total
            subtotal = 0
            # Add Discount
            discount += item.item_discount

        # Final Total
        total = subtotal + platform_fee

    return render(request, "cart.html", {
        "items": items,
        "subtotal": subtotal,
        "discount": discount,
        "platform_fee": platform_fee,
        "total": total,
    })


    

#============================= Delete Cart Item ==========================>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
def remove_cart_item(request, id):
    cart_item = get_object_or_404(CartItem, id=id)
    cart_item.delete()
    return redirect("cart")







#============================= Checkout Cart Item==========================>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
def checkout(request):

    user_id = request.session.get("user_id")

    if not user_id:
        messages.error(request, "Please login first.")
        return redirect("login")

    user = get_object_or_404(Register, id=user_id)

    cart = Cart.objects.filter(
        user=user,
        is_active=True
    ).first()

    if not cart:
        messages.error(request, "Your cart is empty.")
        return redirect("cart")

    items = cart.items.all()

    if not items.exists():
        messages.error(request, "Your cart is empty.")
        return redirect("cart")

    # Calculate total
    subtotal = sum(
        item.product.price * item.quantity
        for item in items
    )

    discount = 0
    platform_fee = 10
    total = subtotal - discount + platform_fee

    # =========================
    # POST = PLACE ORDER
    # =========================
    if request.method == "POST":

        full_name = request.POST.get("full_name")
        phone = request.POST.get("phone")
        address = request.POST.get("address")
        city = request.POST.get("city")
        state = request.POST.get("state")
        pincode = request.POST.get("pincode")

        # Generate unique order number
        order_number = "ORD-" + uuid.uuid4().hex[:10].upper()

        # Create Order
        order = Order.objects.create(
            user=user,
            order_number=order_number,
            total_amount=total,

            full_name=full_name,
            phone=phone,
            address=address,
            city=city,
            state=state,
            pincode=pincode,

            payment_method="PhonePe",
            payment_status="pending",
            order_status="pending"
        )

        # Create Order Items
        for item in items:

            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.price
            )

        # Cart deactivate
        cart.is_active = False
        cart.save()

        messages.success(
            request,
            "Order placed successfully!"
        )

        return redirect("order_success", order_id=order.id)

    return render(request, "checkout.html", {
        "user": user,
        "cart": cart,
        "items": items,
        "subtotal": subtotal,
        "discount": discount,
        "platform_fee": platform_fee,
        "total": total,
    })
