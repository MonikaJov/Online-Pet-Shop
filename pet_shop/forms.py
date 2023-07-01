from django import forms
from .models import Brand, Product, Order, Category, Promotion, UserProfile


class FilterForm(forms.Form):
    price = forms.DecimalField(
        label='Price',
        required=False,
        min_value=1,
        max_value=500,
        widget=forms.NumberInput(attrs={'type': 'range', 'class': 'form-range', 'id': 'price-filter'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        brands = Brand.objects.all()
        choices = [(brand.name, brand.name) for brand in brands]
        self.fields['brand'] = forms.ChoiceField(
            label='Brands',
            required=False,
            choices=choices,
            widget=forms.RadioSelect
        )


class EditProductForm(forms.ModelForm):
    # files = forms.FileField(required=False)

    def __init__(self, *args, **kwargs):
        super(EditProductForm, self).__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"

    class Meta:
        model = Product
        fields = ['name', 'desc', 'keywords', 'category', 'brand', 'price', 'photo', 'promotion', 'has_sizes', 'has_colors']


class CheckoutForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(CheckoutForm, self).__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"

    class Meta:
        model = Order
        exclude = ("user", "cart_products", "date", "processed")


class LoginForm(forms.Form):
    your_username = forms.CharField(label="Username", max_length=100)
    your_password = forms.CharField(label="Password", max_length=100, widget=forms.PasswordInput)


class CategoryForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"

    class Meta:
        model = Category
        fields = ['name', 'photo']


class PromotionForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(PromotionForm, self).__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"

    class Meta:
        model = Promotion
        fields = ['amount', 'duration']


class RegisterForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"

    class Meta:
        model = UserProfile
        exclude = ("user",)
        # fields = ['name', 'surname', 'email', 'address', 'phone_number']