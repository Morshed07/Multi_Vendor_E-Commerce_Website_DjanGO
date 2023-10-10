from django.db import models
from ckeditor.fields import RichTextField
from shortuuid.django_fields import ShortUUIDField
from django.utils.safestring import mark_safe
from userauths.models import User


# Create your models here.

STATUS_CHOICES = (
    ("processing", "Processing"),
    ("shipped", "Shipped"),
    ("delivered", "Delivered")
)


STATUS = (
    ("draft", "Draft"),
    ("disabled", "Disabled"),
    ("rejected", "Rejected"),
    ("in_review", "In Review"),
    ("published", "Published")
)


RATING = (
    (1, "★☆☆☆☆"),
    (2, "★★☆☆☆"),
    (3, "★★★☆☆"),
    (4, "★★★★☆"),
    (5, "★★★★★")
)

def user_directory_path(instance , filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)

class Main_Category(models.Model):
    mcid = ShortUUIDField(
        length=5,
        max_length=10,
        prefix="mcat_",
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
        prefix="cat_",
        alphabet="abcdefg1234",
        unique = True
    )
    m_category = models.ForeignKey(Main_Category, on_delete=models.CASCADE,blank=True,null=True)
    sub_category = models.ForeignKey('self',related_name='subcategory',on_delete=models.CASCADE,blank=True,null=True)
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique=True)
    image = models.ImageField(upload_to='category',blank=True,null=True)
    featured = models.BooleanField(default=False)
    
    class Meta:
        verbose_name_plural = 'Categories'

    def category_image(self):
        return mark_safe('<img src="/media/%s" width = "50" height = "50" />' % (self.image))
    

    def __str__(self) -> str:
        return self.title 
    

    
class Vendor(models.Model):
    vid = ShortUUIDField(
        length=12,
        max_length=20,
        prefix="ven_",
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

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Vendors'

    def vendor_image(self):
        return mark_safe('<img src="/media/%s" width = "50" height = "50" />' % (self.image))


    def __str__(self) -> str:
        return self.name
    
class Tags(models.Model):
    pass
class Sections(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title
    
    
class Product(models.Model):
    pid = ShortUUIDField(
        length=12,
        max_length=20,
        prefix="pro_",
        alphabet="abcdefg1234",
        unique = True
    )
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    title = models.CharField(max_length=250, default='')
    slug= models.SlugField(unique=True, max_length=250)
    image = models.ImageField(upload_to='user_directory_path')
    short_description = RichTextField(blank=True, null= True, default="N/A")
    price = models.IntegerField(default="0")
    old_price = models.IntegerField(default="0")
    product_description = RichTextField(null=True,blank=True)
    
    # tags = models.ForeignKey(Tags, on_delete=models.SET_NULL, null=True)
    product_status = models.CharField(choices=STATUS, max_length=10, default='in_review')
    section = models.ForeignKey(Sections, on_delete=models.CASCADE, blank=True, null=True)
    status = models.BooleanField(default=True)
    in_stock = models.BooleanField(default=True)
    digital = models.BooleanField(default=False)

    sku = ShortUUIDField(
        length=6,
        max_length=10,
        alphabet="12345ABCDEFGH",
        unique = True,
    )

    creatd_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True,blank=True)

    class Meta:
        verbose_name_plural = 'Products'
        ordering = ['-creatd_at']

    def product_image(self):
        return mark_safe('<img src="/media/%s" width = "50" height = "50" />' % (self.image))
        
    def __str__(self) -> str:
        return self.title
        
    def get_percentage(self):
        new_price = ( (self.old_price-self.price) / self.old_price ) * 100
        return new_price
    @property
    def related(self):
        return self.category.products.all().exclude(pk=self.pk)
    
class ProductImages(models.Model):
    images = models.ImageField(upload_to="product_images")
    product = models.ForeignKey(Product, on_delete=models.CASCADE,related_name='product_pics')
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Product Images'

    

class AdditionalInformations(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    
    specifications = models.CharField(max_length=100,null=True,blank=True)
    details = models.CharField(max_length=100,null=True,blank=True)
    class Meta:
        verbose_name_plural = 'Additional Informations'


##########cart, orderitems, order and address###########

class CartOrer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.IntegerField(default="0")
    paid_status = models.BooleanField(default=False)
    order_date = models.DateTimeField(auto_now_add=True)
    product_status = models.CharField(choices=STATUS_CHOICES, max_length=30, default='processing')

    class Meta:
        verbose_name_plural = 'Cart Orders'

class CartOrerItems(models.Model):
    order = models.ForeignKey(CartOrer, on_delete=models.CASCADE)
    invoice_no = models.CharField(max_length=200)
    product_status = models.CharField(max_length=200)
    item = models.CharField(max_length=200)
    image = models.CharField(max_length=200)
    qty = models.IntegerField(default=0)
    price = models.IntegerField( default="0")
    total = models.IntegerField( default="0")

    class Meta:
        verbose_name_plural = 'Cart Order Items'

    def orderitems_images(self):
        return mark_safe('<img src="/media/%s" width = "50" height = "50" />' % (self.image))
    
class ProductReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null= True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null= True)
    review = models.TextField()
    rating = models.IntegerField(choices=RATING, default=None)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Product Review'
        
    def __str__(self) -> str:
        return self.product.title

    def get_rating(self):
        return self.rating


class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null= True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null= True)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Wishlists'
        
    def __str__(self) -> str:
        return self.product.title

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null= True)
    address = models.CharField(max_length=200,null=True)
    status = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Addresses'

class Slider(models.Model):
    brand = models.CharField(max_length=50,blank=True,null=True)
    title = models.CharField(max_length=100,blank=True,null=True)
    slogan = models.CharField(max_length=100,blank=True,null=True)
    image = models.ImageField(upload_to='sliders')
    active = models.BooleanField(default=True)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Sliders'

    def slider_images(self):
        return mark_safe('<img src="/media/%s" width = "70 height = "70" />' % (self.image))
    
    def __str__(self) -> str:
        return self.brand
    
class TopBanner(models.Model):
    type = models.CharField(max_length=50,blank=True,null=True)
    title = models.CharField(max_length=100,blank=True,null=True)
    deal_percent = models.CharField(max_length=10,blank=True,null=True)
    image = models.ImageField(upload_to='topbanners')
    active = models.BooleanField(default=True)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Top Banners'

    def topbanner_images(self):
        return mark_safe('<img src="/media/%s" width = "70 height = "70" />' % (self.image))
    
    def __str__(self) -> str:
        return self.title