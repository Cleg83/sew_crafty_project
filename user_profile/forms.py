from django import forms
from .models import UserProfile


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Make the email field read-only
        if 'default_email' in self.fields:
            self.fields['default_email'].widget.attrs['readonly'] = True
            # Add a custom note below the email field
            self.fields['default_email'].help_text = "Please email sewcrafty.amin@proton.me to update your email address."

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
            'default_email': 'Email',  # Keep placeholder for consistency
        }

        for field in self.fields:
            if field != 'default_country':
                placeholder = f'{placeholders.get(field, "")} *' if self.fields[field].required else placeholders.get(field, "")
                self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].label = False

    def save(self, commit=True):
        user_profile = super().save(commit=False)
        user = user_profile.user  # Get the linked User instance

        user.first_name = self.cleaned_data.get('default_first_name') or ''
        user.last_name = self.cleaned_data.get('default_last_name') or ''
        # Do NOT update email

        if commit:
            user.save()
            user_profile.save()

        return user_profile


