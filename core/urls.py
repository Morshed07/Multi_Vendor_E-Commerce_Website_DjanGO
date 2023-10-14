from django.urls import path
from .views import(
    HomeView,
    ProductListView,
    ProductDetails,
    Tag_List,
    SearchProducts
)
urlpatterns = [
    path('',HomeView.as_view(), name = 'home' ),
    path('products/',ProductListView.as_view(), name = 'products-list' ),
    path('products/tag-products/<slug:tag_slug>/',Tag_List, name = 'tag-products-list' ),
    path('product-details/<slug:slug>/',ProductDetails.as_view(), name = 'product-details' ),
    path('search-products/',SearchProducts.as_view(), name='search-products'),

]