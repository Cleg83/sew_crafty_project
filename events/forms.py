from django import forms
from .models import Events

class EventForm(forms.ModelForm):
    class Meta:
        model = Events
        fields = [
            'name', 'start_date', 'end_date', 'start_time', 'end_time', 
            'description', 'location', 'image_url', 'image', 'ticket_required', 'ticket_url'
        ]
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
            'description': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Event Description'}),
            'location': forms.TextInput(attrs={'placeholder': 'Event Location'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Set placeholders for fields
        self.fields['name'].widget.attrs['placeholder'] = 'Event Name'
        self.fields['ticket_required'].widget.attrs['class'] = 'form-check-input'
        self.fields['image'].widget.attrs['accept'] = 'image/*'
        self.fields['image_url'].widget.attrs['placeholder'] = 'Event Image URL (optional)'
        self.fields['ticket_url'].widget.attrs['placeholder'] = 'Event Ticket URL (optional)'

        # Optional: Apply any other specific styling or attributes as needed
        for field in self.fields:
            if self.fields[field].required:
                self.fields[field].widget.attrs['class'] = 'form-control required'
            else:
                self.fields[field].widget.attrs['class'] = 'form-control'
