

from django import forms


class CheckoutForm(forms.Form):
    PAYMENT_METHODS = [
        ("COD", "Cash on delivery"),
        ("ONLINE", "Online payment"),
    ]

    name = forms.CharField(max_length=100)
    phone_number = forms.CharField(max_length=15)
    address = forms.CharField(widget=forms.Textarea(attrs={"rows": 3}))
    payment_method = forms.ChoiceField(
        choices=PAYMENT_METHODS,
        widget=forms.RadioSelect,
        initial="COD",
    )