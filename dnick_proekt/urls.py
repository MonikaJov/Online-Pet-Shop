"""
URL configuration for dnick_proekt project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from pet_shop import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('checkout/', views.checkout, name='checkout'),
    path('home/', views.home, name='home'),
    path('cart/', views.cart, name='cart'),
    path('register/', views.register, name='register'),
    path('remove_promotion/<int:product_id>/', views.remove_promotion, name='remove_promotion'),
    path('add_promotion/<int:product_id>/', views.add_promotion, name='add_promotion'),
    path('add_category/', views.add_category, name='add_category'),
    path('remove_category/<int:category_id>/', views.remove_category, name='remove_category'),
    path('products/search/', views.search_results, name='search_results'),
    path('logout_form/', views.logout_form, name='logout_form'),
    path('login_form/', views.login_form, name='login_form'),
    path('view_orders/', views.view_orders, name='view_orders'),
    path('create/', views.create_product, name='create'),
    path('<str:category>/', views.category_view, name='category_view'),
    path('edit/<int:product_id>/', views.edit, name='edit'),
    path('delete/<int:product_id>/', views.delete, name='delete'),
    path('view/<int:product_id>/', views.view, name='view_product'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)