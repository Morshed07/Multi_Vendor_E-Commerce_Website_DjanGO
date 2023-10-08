from django.db.models import Count
from django.shortcuts import render
from django.db.models import Q
from typing import Any, Dict
from django.shortcuts import render
from django.views.generic import (
    TemplateView,
    DetailView,
    ListView,
    View,
)
from .models import (
    Main_Category,
    Category,
    Product,
    Slider,
    TopBanner
    
)

class Home(TemplateView):
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
    