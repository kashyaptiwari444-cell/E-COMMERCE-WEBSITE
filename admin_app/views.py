from django.shortcuts import render, redirect
from .models import Product, Category, SubCategory, Brand
from django.utils.text import slugify

def admin_dash(request):
    return render(request, 'admin_dash.html')
    

#============================== Add Product ===========================>>>>>>>>>>>>>>>>

def add_product(request):

    if request.method == "POST":
    
            product_name = request.POST.get("product_name")
            slug = request.POST.get("slug")
    
            if not slug:
                slug = slugify(product_name)
    
            category_name = request.POST.get("category")
            subcategory_name = request.POST.get("subcategory")
            brand_name = request.POST.get("brand")
    
            description = request.POST.get("description")
            price = request.POST.get("price")
            discount_price = request.POST.get("discount_price")
            stock = request.POST.get("stock")
            rating = request.POST.get("rating") or 0
    
            status = request.POST.get("status") == "Active"
    
            image = request.FILES.get("image")
    
            # Create if doesn't exist
            category, created = Category.objects.get_or_create(
                category_name=category_name,
                defaults={
                    "slug": slugify(category_name)
                }
            )

            subcategory, created = SubCategory.objects.get_or_create(
                name=subcategory_name,
                category=category,
                defaults={
                    "slug": slugify(subcategory_name)
                }
            )

            brand, created = Brand.objects.get_or_create(
                name=brand_name,
                defaults={
                    "slug": slugify(brand_name)
                }
            )
    
            Product.objects.create(
                category=category,
                subcategory=subcategory,
                brand=brand,
                product_name=product_name,
                slug=slug,
                description=description,
                price=price,
                discount_price=discount_price if discount_price else None,
                stock=stock,
                rating=rating,
                status=status,
                image=image,
            )
    
            return redirect("view_product")
    
    return render(request, "products/add_product.html")





#============================== View Product ===========================>>>>>>>>>>>>>>>>

def view_product(request):
    products = Product.objects.select_related(
        "category",
        "subcategory",
        "brand"
    ).all().order_by("-id")

    return render(request, "products/view_product.html", {"products":products})
    


#============================== Edit Product ===========================>>>>>>>>>>>>>>>>


from django.shortcuts import render, redirect, get_object_or_404
from django.utils.text import slugify
from .models import Product, Category, SubCategory, Brand


def edit_product(request, id):

    product = get_object_or_404(Product, id=id)

    if request.method == "POST":

        product_name = request.POST.get("product_name")
        slug = request.POST.get("slug")

        if not slug:
            slug = slugify(product_name)

        category_name = request.POST.get("category")
        subcategory_name = request.POST.get("subcategory")
        brand_name = request.POST.get("brand")

        description = request.POST.get("description")
        price = request.POST.get("price")
        discount_price = request.POST.get("discount_price")
        stock = request.POST.get("stock")
        rating = request.POST.get("rating") or 0

        status = request.POST.get("status") == "Active"

        image = request.FILES.get("image")

        # Category
        category, _ = Category.objects.get_or_create(
            category_name=category_name,
            defaults={
                "slug": slugify(category_name)
            }
        )

        # SubCategory
        subcategory, _ = SubCategory.objects.get_or_create(
            name=subcategory_name,
            category=category,
            defaults={
                "slug": slugify(subcategory_name)
            }
        )

        # Brand
        brand, _ = Brand.objects.get_or_create(
            name=brand_name,
            defaults={
                "slug": slugify(brand_name)
            }
        )

        # Update Product
        product.product_name = product_name
        product.slug = slug
        product.category = category
        product.subcategory = subcategory
        product.brand = brand
        product.description = description
        product.price = price
        product.discount_price = discount_price if discount_price else None
        product.stock = stock
        product.rating = rating
        product.status = status

        if image:
            product.image = image

        product.save()

        return redirect("view_product")

    return render(request, "products/edit_product.html", {
        "product": product
    })
    
    
    
    
    
    

#============================== delete Product ===========================>>>>>>>>>>>>>>>>

    
def delete_product(request, id):
    product = get_object_or_404(Product, id=id)
    product.delete()

    return redirect("view_product")



#============================== Add Category ===========================>>>>>>>>>>>>>>>>

def add_category(request):
    
    if request.method == "POST":
        category_name = request.POST.get("category_name")
        slug = request.POST.get("slug")

        if not slug:
            slug = slugify(category_name)

        description = request.POST.get("description")
        image = request.FILES.get("image")
        status = request.POST.get("status") == "Active"

        Category.objects.create(
            category_name=category_name,
            slug=slug,
            description=description,
            image=image,
            status=status,
        )

        return redirect("admin_dash")

    return render(request, "category/add_category.html")



#============================== View Category ===========================>>>>>>>>>>>>>>>>

def view_category(request):
    categories = Category.objects.all().order_by("-id")
    return render(request, "category/view_category.html", {
        "categories": categories
    })
    
    



# ============================== Edit Category ==============================>>>>>>>>>>>>>>>>

def edit_category(request, id):

    category = get_object_or_404(Category, id=id)

    if request.method == "POST":

        category.category_name = request.POST.get("category_name")

        slug = request.POST.get("slug")
        if not slug:
            slug = slugify(category.category_name)

        category.slug = slug

        category.description = request.POST.get("description")

        category.status = request.POST.get("status") == "Active"

        image = request.FILES.get("image")
        if image:
            category.image = image

        category.save()

        return redirect("view_category")

    return render(request, "category/edit_category.html", {
        "category": category
    })
    
    
  

# ============================== Delete Category ==============================>>>>>>>>>
    
def delete_category(request, id):
    category = get_object_or_404(Category, id=id)
    category.delete()

    return redirect("view_category")




# ============================== Add Brand ==============================>>>>>>>>>
    
def add_brand(request):
    if request.method == "POST":
        Brand.objects.create(
            name=request.POST.get("name"),
            slug=request.POST.get("slug"),
            logo=request.FILES.get("logo"),
            description=request.POST.get("description"),
            status=request.POST.get("status") == "True"
        )
        return redirect("admin_dash")

    return render(request, "brands/add_brand.html")





#============================== View Brand ===========================>>>>>>>>>>>>>>>>

def view_brand(request):
    brands = Brand.objects.all().order_by("-id")
    return render(request, "brands/view_brand.html", {
        "brands": brands
    })
    
    


#============================== Edit Brand ===========================>>>>>>>>>>>>>>>>

def edit_brand(request, id):
    brand = get_object_or_404(Brand, id=id)

    if request.method == "POST":
        brand.name = request.POST.get("name")
        brand.slug = request.POST.get("slug")
        brand.description = request.POST.get("description")
        brand.status = request.POST.get("status") == "True"

        if request.FILES.get("logo"):
            brand.logo = request.FILES["logo"]

        brand.save()
        return redirect("view_brand")

    return render(request, "brands/edit_brand.html", {"brand": brand})





# ============================== Delete Brand ==============================>>>>>>>>>
    
def delete_brand(request, id):
    brand = get_object_or_404(Brand, id=id)
    brand.delete()

    return redirect("view_brand")
