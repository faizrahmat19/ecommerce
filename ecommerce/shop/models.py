from django.db import models
from django.utils.text import slugify
from db.models import User #import kustom user dari app db


#model cateogry one-to-many
class Kategori(models.Model):
    name = models.CharField(max_length=10, unique=True, verbose_name="Nama Kategori")
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(verbose_name="Deskripsi", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Dibuat pada")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Diperbarui pada")
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=False, verbose_name="Harga")

    class Meta:
        verbose_name = "Kategori"
        verbose_name_plural = "Kategori"
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

#model produk one-to-many
class Product(models.Model):
    name = models.TextField(unique=True, verbose_name="Nama Produk")
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(verbose_name="Deskripsi", blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Harga")
    category = models.ForeignKey(Kategori, on_delete=models.CASCADE, related_name='products', verbose_name="Kategori")
    stock_produk = models.PositiveIntegerField(verbose_name="Stok")
    stock_diskon = models.PositiveIntegerField(verbose_name="Stok Diskon")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Dibuat pada")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Diperbarui pada")    
    is_active = models.BooleanField(default=True, verbose_name="Aktif")

    class Meta:
        verbose_name = "Produk"
        verbose_name_plural = "Produk"
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
#model keranjang
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="User")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Dibuat Pada")

    class Meta:
        verbose_name = 'Cart'
        verbose_name_plural = 'Cart'

    def __str__(self):
        return f"Cart {self.user.username}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items', verbose_name="Cart")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Produk")
    quantity = models.PositiveIntegerField(verbose_name="Jumlah")

    class Meta:
        verbose_name = 'Cart Item'
        verbose_name_plural = 'Cart Item'

    def __str__(self):
        return f"{self.quantity} of {self.product.name}"

#model pesanan
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='OrderItem', related_name='orders', verbose_name="Produk")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Total Harga")
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20, 
        choices=[
        ('PENDING', 'Pending'), 
        ('SHIPPED', 'Shipped'), 
        ('DELIVERED', 'Delivered'),
        ],
        default='PENDING',
        verbose_name="Status"
    )

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Order'

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"

#Model detail pesanan
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items', verbose_name="Order")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Produk")
    quantity = models.PositiveIntegerField(verbose_name="Jumlah")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Harga")

    class Meta:
        verbose_name = 'Order Item'
        verbose_name_plural = 'Order Item'

    def __str__(self):
        return f"{self.quantity} of {self.product.name}"


# Create your models here.
