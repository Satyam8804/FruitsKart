from django import forms
from .models import Order


class CartForm(forms.Form):
    quantity = forms.IntegerField(initial='1')
    product_id = forms.IntegerField(widget=forms.HiddenInput)

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(CartForm, self).__init__(*args, **kwargs)


class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        exclude = ('paid',)
        widgets = {
            'address': forms.Textarea(attrs={'rows': 2, 'cols': 40}),  # Use 'rows' and 'cols' instead of 'row' and 'col'
        }
