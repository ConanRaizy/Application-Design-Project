from django import forms
from .models import Car, Review


INPUT_CLASS = 'form-input'
TEXTAREA_CLASS = 'form-input'


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['make', 'model', 'year', 'price', 'mileage', 'fuel_type', 'color', 'status', 'description']
        widgets = {
            'make':        forms.TextInput(attrs={'class': INPUT_CLASS, 'placeholder': 'e.g. BMW'}),
            'model':       forms.TextInput(attrs={'class': INPUT_CLASS, 'placeholder': 'e.g. 3 Series'}),
            'year':        forms.NumberInput(attrs={'class': INPUT_CLASS, 'placeholder': '2023'}),
            'price':       forms.NumberInput(attrs={'class': INPUT_CLASS, 'placeholder': '25000'}),
            'mileage':     forms.NumberInput(attrs={'class': INPUT_CLASS, 'placeholder': '15000'}),
            'fuel_type':   forms.Select(attrs={'class': INPUT_CLASS}),
            'color':       forms.TextInput(attrs={'class': INPUT_CLASS, 'placeholder': 'e.g. Midnight Black'}),
            'status':      forms.Select(attrs={'class': INPUT_CLASS}),
            'description': forms.Textarea(attrs={'class': TEXTAREA_CLASS, 'rows': 4, 'placeholder': 'Vehicle description...'}),
        }


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['customer_name', 'customer_email', 'car', 'rating', 'title', 'review_text']
        widgets = {
            'customer_name':  forms.TextInput(attrs={'class': INPUT_CLASS, 'placeholder': 'Your full name'}),
            'customer_email': forms.EmailInput(attrs={'class': INPUT_CLASS, 'placeholder': 'your@email.com'}),
            'car':            forms.Select(attrs={'class': INPUT_CLASS}),
            'rating':         forms.Select(attrs={'class': INPUT_CLASS}),
            'title':          forms.TextInput(attrs={'class': INPUT_CLASS, 'placeholder': 'Review title'}),
            'review_text':    forms.Textarea(attrs={'class': TEXTAREA_CLASS, 'rows': 5, 'placeholder': 'Share your experience...'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['car'].required = False
        self.fields['car'].empty_label = '— General enquiry —'


class AdminCommentForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['admin_comment', 'is_approved']
        widgets = {
            'admin_comment': forms.Textarea(attrs={
                'class': TEXTAREA_CLASS,
                'rows': 5,
                'placeholder': 'Write your response to this review...',
            }),
            'is_approved': forms.CheckboxInput(attrs={'style': 'accent-color: var(--gold);'}),
        }
