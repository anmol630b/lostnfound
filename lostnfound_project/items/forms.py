from django import forms
from .models import Item, ClaimRequest


class ItemForm(forms.ModelForm):
    date_lost_found = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        label="Date Lost/Found"
    )

    class Meta:
        model = Item
        fields = ['title', 'description', 'category', 'item_type',
                  'location', 'location_detail', 'date_lost_found',
                  'image', 'contact_email', 'contact_phone']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Black iPhone 14, Blue Backpack'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Describe color, brand, unique marks...'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'item_type': forms.Select(attrs={'class': 'form-select'}),
            'location': forms.Select(attrs={'class': 'form-select'}),
            'location_detail': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Near entrance, 2nd floor'}),
            'image': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'contact_email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'your@email.com'}),
            'contact_phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 9876543210 (for WhatsApp contact)'}),
        }


class SearchForm(forms.Form):
    query = forms.CharField(required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Search items...'}))
    item_type = forms.ChoiceField(required=False,
        choices=[('', 'All Items'), ('lost', 'Lost'), ('found', 'Found')],
        widget=forms.Select(attrs={'class': 'form-select'}))
    category = forms.ChoiceField(required=False,
        choices=[('', 'All Categories')] + Item.CATEGORY_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}))
    location = forms.ChoiceField(required=False,
        choices=[('', 'All Locations')] + Item.LOCATION_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}))


class ClaimForm(forms.ModelForm):
    class Meta:
        model = ClaimRequest
        fields = ['message', 'contact_phone', 'contact_email']
        widgets = {
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 5,
                'placeholder': 'Describe proof of ownership: serial number, unique features, etc.'}),
            'contact_phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your WhatsApp/phone number'}),
            'contact_email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your email'}),
        }
