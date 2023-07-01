from django.contrib import admin
from .models import Product, Promotion, CartProduct, Order, Cart, Category, Brand, UserProfile, SuperUser, OrderedProducts


class CartProductAdmin(admin.ModelAdmin):
    exclude = ("user",)

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        return super().save_model(request, obj, form, change)


admin.site.register(CartProduct,  CartProductAdmin)


class OrderAdmin(admin.ModelAdmin):
    exclude = ("user",)

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        return super().save_model(request, obj, form, change)


admin.site.register(Order, OrderAdmin)


class CartAdmin(admin.ModelAdmin):
    exclude = ("user",)

    def save_model(self, request, obj, form, change):
        return super().save_model(request, obj, form, change)


admin.site.register(Cart, CartAdmin)

admin.site.register(Brand)
admin.site.register(Promotion)
admin.site.register(UserProfile)
admin.site.register(SuperUser)
admin.site.register(Category)
admin.site.register(Product)


class OrderedProductsAdmin(admin.ModelAdmin):
    exclude = ("user",)

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        return super().save_model(request, obj, form, change)


admin.site.register(OrderedProducts, OrderedProductsAdmin)
