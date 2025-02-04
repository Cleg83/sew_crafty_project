from django import forms
from .models import Product, Category

class AddProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['category', 'sku', 'name', 'description', 'price', 'image', 'in_stock']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        categories = Category.objects.all()
        display_names = [(c.id, c.get_display_name() or c.name) for c in categories]
        self.fields['category'].choices = display_names

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price <= 0:
            raise forms.ValidationError("Price must be greater than zero.")
        return price


class AddCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'display_name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['display_name'].widget.attrs.update({'class': 'form-control'})
