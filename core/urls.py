from django.urls import path
from .views import(
    HomeView,
    ProductListView,
    ProductDetails,
       
)
urlpatterns = [
    path('',HomeView.as_view(), name = 'home' ),
    path('products/',ProductListView.as_view(), name = 'products-list' ),
    path('product-details/<slug:slug>/',ProductDetails.as_view(), name = 'product-details' ),
]