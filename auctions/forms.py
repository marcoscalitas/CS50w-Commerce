from django import forms
from .models import Listing, Bid, Comment
from django import forms

IS_INVALID = "is-invalid"
INPUT_CLASS = "form-control"


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(
            attrs={"class": INPUT_CLASS, "placeholder": "Username", "required": True}
        ),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": INPUT_CLASS, "placeholder": "Password", "required": True}
        )
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        fields_to_check = ["username", "password"]

        for field_name in fields_to_check:
            if self.errors.get(field_name):
                self.fields[field_name].widget.attrs["class"] += f" {IS_INVALID}"


class RegisterForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": INPUT_CLASS,
                "placeholder": "Username",
                "required": True,
            }
        ),
        label="Username",
    )

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "class": INPUT_CLASS,
                "placeholder": "Email Address",
                "required": True,
            }
        ),
        label="Email Address",
    )

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": INPUT_CLASS,
                "placeholder": "Password",
                "required": True,
            }
        ),
        label="Password",
    )

    confirmation = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": INPUT_CLASS,
                "placeholder": "Confirm Password",
                "required": True,
            }
        ),
        label="Confirm Password",
    )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirmation = cleaned_data.get("confirmation")

        if password and confirmation and password != confirmation:
            self.add_error(None, "Passwords must match.")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name in self.fields:
            if field_name in self.errors:
                self.fields[field_name].widget.attrs["class"] += f" {IS_INVALID}"


class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = [
            "title",
            "description",
            "price",
            "image_url",
            "category",
        ]  # Inclui o campo de categoria
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Title",
                    "autofocus": "autofocus",
                    "required": True,
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Description",
                    "required": True,
                    "rows": 3,
                }
            ),
            "price": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Price",
                    "required": True,
                }
            ),
            "image_url": forms.URLInput(
                attrs={"class": "form-control", "placeholder": "Image URL"}
            ),
            "category": forms.Select(
                attrs={
                    "class": "form-control",
                    "aria-label": "Default select example",
                    "required": True,
                }
            ),
        }

    def clean(self):
        cleaned_data = super().clean()
        price = cleaned_data.get("price")

        if price:
            try:
                price = float(price)
                if price <= 0:
                    self.add_error("price", "Price must be a positive number.")
            except ValueError:
                self.add_error("price", "Price must be a valid number.")

        return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name in self.fields:
            if field_name in self.errors:
                self.fields[field_name].widget.attrs["class"] += f" {IS_INVALID}"


class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ["amount"]
        widgets = {
            "amount": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter your bid amount",
                    "required": True,
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name in self.fields:
            if field_name in self.errors:
                self.fields[field_name].widget.attrs["class"] += f" {IS_INVALID}"


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]  # Inclui os campos que deseja no formulário
        widgets = {
            "content": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter your comment",
                    "required": True,
                    "rows": 3,
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name in self.fields:
            if field_name in self.errors:
                self.fields[field_name].widget.attrs["class"] += f" {IS_INVALID}"
