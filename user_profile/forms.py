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

    # def save(self, commit=True):
    #     user_profile = super().save(commit=False)
    #     user = user_profile.user  # Get the linked User instance

    #     # Update the User model fields
    #     user.first_name = self.cleaned_data['default_first_name']
    #     user.last_name = self.cleaned_data['default_last_name']
    #     user.email = self.cleaned_data['default_email']

    #     if commit:
    #         user.save()  # Save the User instance
    #         user_profile.save()  # Save the UserProfile instance

    #     return user_profile

    def save(self, commit=True):
        user_profile = super().save(commit=False)
        user = user_profile.user  # Get the linked User instance

        # Ensure None values are saved as empty strings
        user.first_name = self.cleaned_data.get('default_first_name') or ''
        user.last_name = self.cleaned_data.get('default_last_name') or ''
        user.email = self.cleaned_data.get('default_email') or ''

        if commit:
            user.save()  # Save the User instance
            user_profile.save()  # Save the UserProfile instance

        return user_profile

