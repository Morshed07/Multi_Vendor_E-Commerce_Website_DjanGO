from django.db import models
from djrichtextfield.models import RichTextField
from shortuuid.django_fields import ShortUUIDField
from django.utils.safestring import mark_safe
from userauths.models import User


# Create your models here.

def user_directory_path(instance , filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)

class Main_Category(models.Model):
    mcid = ShortUUIDField(
        length=5,
        max_length=10,
        prefix="mcat",
        alphabet="abcdefg1234",
        unique = True
    )
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    
    class Meta:
        verbose_name_plural = 'Main Categories'


    def __str__(self) -> str:
        return self.title

class Category(models.Model):
    cid = ShortUUIDField(
        length=12,
        max_length=20,
        prefix="cat",
        alphabet="abcdefg1234",
        unique = True
    )
    m_category = models.ForeignKey(Main_Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique=True)
    image = models.ImageField(upload_to='category')
    featured = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Categories'

    def category_image(self):
        return mark_safe('<img src="/media/%s" width = "50" height = "50" />' % (self.image))


    def __str__(self) -> str:
        return self.title
    
class Sub_Category(models.Model):
    scid = ShortUUIDField(
        length=12,
        max_length=20,
        prefix="scat",
        alphabet="abcdefg1234",
        unique = True
    )
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = 'Sub Categories'


    def __str__(self) -> str:
        return self.title
    
class Vendor(models.Model):
    vid = ShortUUIDField(
        length=12,
        max_length=20,
        prefix="ven",
        alphabet="abcdefg1234",
        unique = True
    )
    name = models.CharField(max_length=250)
    image = models.ImageField(upload_to='user_directory_path')
    description = RichTextField(blank=True, null=True)

    address = models.CharField(max_length=150)
    contact = models.CharField(max_length=16, default= '+880')
    chat_resp_time = models.CharField(max_length=100, default="100")
    shipping_on_time = models.CharField(max_length=100, default="100")
    authentic_rating = models.CharField(max_length=100, default="100")
    days_return = models.CharField(max_length=100, default="100")
    warranty_period = models.CharField(max_length=100, default="100")

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name_plural = 'Vendors'

    def vendor_image(self):
        return mark_safe('<img src="/media/%s" width = "50" height = "50" />' % (self.image))


    def __str__(self) -> str:
        return self.name
    
class Tags(models.Model):
    pass
    
class Product(models.Model):
    pid = ShortUUIDField(
        length=12,
        max_length=20,
        prefix="prod",
        alphabet="abcdefg1234",
        unique = True
    )
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null= True, related_name="products")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null= True)

    name = models.CharField(max_length=250, default='product name')
    slug= models.SlugField(unique=True, max_length=250)
    image = models.ImageField(upload_to='product_images')
    description = RichTextField(blank=True, null= True, default="N/A")
    price = models.IntegerField(max_digits=9999999999, default="0")
    old_price = models.IntegerField(max_digits=9999999999, default="0")
    specifications = RichTextField(null=True,blank=True)
    tags = models.ForeignKey(Tags, on_delete=models.SET_NULL, null=True)
    product_status = models.CharField(choices=STATUS, max_length=10, default='in_review')

    status = models.BooleanField(default=True)
    in_stock = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    top_rated = models.BooleanField (default=False)
    on_sale = models.BooleanField(default=False)
    digital = models.BooleanField(default=False)

    creatd_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True,blank=True)

    class Meta:
        verbose_name_plural = 'Products'
        ordering = ['-creatd_at']

    def product_image(self):
        return mark_safe('<img src="/media/%s" width = "50" height = "50" />' % (self.image))
        
    def __str__(self) -> str:
        return self.title
        
    def get_percetage(self):
        new_price = (self.price / self.old_price) * 100
        return new_price