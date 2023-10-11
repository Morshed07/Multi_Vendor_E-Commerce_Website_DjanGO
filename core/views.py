from django.shortcuts import get_object_or_404
from django.db.models import Count
from django.forms import SlugField
from django.shortcuts import render
from django.db.models import Q
from typing import Any, Dict, Self
from taggit.models import Tag
from django.views.generic import (
    TemplateView,
    DetailView,
    ListView,
)
from .models import (
    Main_Category,
    Category,
    Product,
    Slider,
    TopBanner,
    ProductImages,
    AdditionalInformations,
)

class HomeView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context  = super().get_context_data(**kwargs) 
        context['products'] = Product.objects.all()
        
        context.update(
            {
                "maincats": Main_Category.objects.all(),
                "sliders" : Slider.objects.filter(active=True)[0:3],
                "topbanners" : TopBanner.objects.filter(active=True)[0:10],
                "featured_categories": Category.objects.filter(featured=True),
                "featured_products" : Product.objects.filter(section__title="Featured"),    
                "top_rated": Product.objects.filter(section__title="Top-Rated"),
                "on_sale": Product.objects.filter(section__title="On-Sale")
            }
        )
        return context
    
class ProductListView(ListView):
    model = Product
    template_name = "products/products_list.html"
    context_object_name = 'products_list'

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)
        


class ProductDetails(DetailView):
    model = Product
    template_name = "products/product_details.html"
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['related_products'] = self.get_object().related
        context['images'] = ProductImages.objects.filter(product=self.object)
        context['add_inform'] = AdditionalInformations.objects.filter(product=self.object)
        return context
    
def Tag_List(request, tag_slug=None):
    products = Product.objects.filter(product_status = "published").order_by("-id")

    tag = None
    if tag_slug :
        tag = get_object_or_404(Tag, slug = tag_slug)
        products= Product.objects.filter(tags__in=[tag])

        context = {
            "products" : products,
            "tag": tag
        }
    return render(request,'products/tag_products.html',context)

        