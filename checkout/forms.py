from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('first_name', 'last_name', 'email', 
                  'phone_number', 'address_1', 'address_2', 
                  'town', 'postcode', 'county', 'country')

    def __init__(self, *args, **kwargs):
        """
        Add placeholders, classes, and auto-focus where appropriate.
        """
        super().__init__(*args, **kwargs)

        # Dictionary for placeholders and additional field attributes
        self.field_options = {
            'first_name': {
                'placeholder': 'First Name',
                'autofocus': True,
            },
            'last_name': {
                'placeholder': 'Last Name',
            },
            'email': {
                'placeholder': 'Email Address',
            },
            'phone_number': {
                'placeholder': 'Phone Number',
            },
            'address_1': {
                'placeholder': 'Address',
            },
            'address_2': {
                'placeholder': 'Address continued',
            },
            'town': {
                'placeholder': 'Town, City, or Village',
            },
            'postcode': {
                'placeholder': 'Postcode',
            },
            'county': {
                'placeholder': 'County or State',
            },
            'country': {
                'placeholder': 'Select a Country',
            },
        }

        # Loop through each field to apply custom options
        for field_name, options in self.field_options.items():
            if field_name in self.fields:
                field = self.fields[field_name]

                # Set placeholder if specified
                if 'placeholder' in options:
                    field.widget.attrs['placeholder'] = options['placeholder']

                # Set autofocus on first field
                if 'autofocus' in options:
                    field.widget.attrs['autofocus'] = 'autofocus'

                # Set CSS class for styling
                field.widget.attrs['class'] = 'stripe-formatting'

                # Remove the label
                field.label = False