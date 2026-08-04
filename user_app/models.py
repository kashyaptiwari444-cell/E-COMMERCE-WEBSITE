from django.db import models
from django.contrib.auth.models import User
from admin_app.models import Product

# Create your models here.

class Register(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    gender = models.CharField(max_length=20)
    phone = models.CharField(max_length=12)
    course = models.CharField(max_length=100)
    qualification = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='photos/')
    address = models.TextField()
    pwd = models.TextField()

    def __str__(self):
        return self.name
    
    
    
    
class Cart(models.Model):
    user = models.OneToOneField(
        Register,
        on_delete=models.CASCADE,
        related_name="cart"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.user.name




class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name="items"
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    quantity = models.PositiveIntegerField(default=1)

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    


    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.total_price = self.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return self.product.product_name