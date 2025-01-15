from django import forms
from .models import UserProfile


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Placeholder text for the fields
        placeholders = {
            'default_phone_number': 'Phone Number',
            'default_postcode': 'Postcode',
            'default_town': 'Town, City or Village etc.',
            'default_address_1': 'Address',
            'default_address_2': 'Address continued',
            'default_county': 'County or State etc.',
            'default_country': 'Country',
            'default_first_name': 'First Name',
            'default_last_name': 'Last Name',
            'default_email': 'Email',
        }

        # Set placeholders for each field
        for field in self.fields:
            if field != 'default_country':    
                if self.fields[field].required:
                    placeholder = f'{placeholders.get(field, "")} *'
                else:
                    placeholder = placeholders.get(field, "")
                self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].label = False
