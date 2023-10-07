from django.contrib import admin
from .models import(
    Address,
    Wishlist,
    ProductReview,
    CartOrerItems,
    CartOrer,
    ProductImages,
    Product,
    Vendor,
    Category,
    Main_Category,
    AdditionalInformations,
    Sections,
    Slider,
    TopBanner,


)

# Register your models here.

class SliderAdmin(admin.ModelAdmin):
    list_display = ['brand','title','slider_images','active','date']

class TopBannerAdmin(admin.ModelAdmin):
    list_display = ['title','topbanner_images','active','date']

class ProductImagesAdmin(admin.TabularInline):
    model = ProductImages
class AdditionalInformationAdmin(admin.TabularInline):
    model = AdditionalInformations

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImagesAdmin, AdditionalInformationAdmin]
    prepopulated_fields = {"slug": ('title',)}
    list_display = ['user','title','product_image','price', 'product_status','section']
    # list_editable = ['section','product_status']

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ('title',)}
    list_display = [  'title','category_image', 'featured']

class Main_CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ('title',)}
    list_display = [ 'mcid', 'title']


class VendorAdmin(admin.ModelAdmin):
    list_display = ['name', 'vendor_image']

class CartOrerAdmin(admin.ModelAdmin):
    list_display = ['user','price','paid_status','product_status','order_date']


class CartOrerItemsAdmin(admin.ModelAdmin):
    list_display = ['order','invoice_no','item', 'orderitems_images','qty', 'price', 'total']

class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ['user','product','review', 'rating']

class WishlistAdmin(admin.ModelAdmin):
    list_display = ['user','product','date']

class AddressAdmin(admin.ModelAdmin):
    list_display = ['user','address','status']

admin.site.register(Sections)
admin.site.register(Slider,SliderAdmin)
admin.site.register(TopBanner,TopBannerAdmin)
admin.site.register(Product,ProductAdmin)
admin.site.register(Vendor,VendorAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(Main_Category,Main_CategoryAdmin)
admin.site.register(CartOrer,CartOrerAdmin)
admin.site.register(CartOrerItems,CartOrerItemsAdmin)
admin.site.register(ProductReview,ProductReviewAdmin)
admin.site.register(Wishlist,WishlistAdmin)
admin.site.register(Address,AddressAdmin)
