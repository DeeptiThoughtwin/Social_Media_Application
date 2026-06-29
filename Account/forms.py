
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .models import Profile



class RegistrationForm(UserCreationForm):

    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Username",
                "class": "w-full rounded-lg border border-pink-300 px-4 py-3 focus:outline-none focus:ring-2 focus:ring-pink-400"
            }
        )
    )

    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "First Name",
                "class": "w-full rounded-lg border border-pink-300 px-4 py-3 focus:outline-none focus:ring-2 focus:ring-pink-400"
            }
        )
    )

    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Last Name",
                "class": "w-full rounded-lg border border-pink-300 px-4 py-3 focus:outline-none focus:ring-2 focus:ring-pink-400"
            }
        )
    )

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Email Address",
                "class": "w-full rounded-lg border border-pink-300 px-4 py-3 focus:outline-none focus:ring-2 focus:ring-pink-400"
            }
        )
    )

    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "w-full rounded-lg border border-pink-300 px-4 py-3 focus:outline-none focus:ring-2 focus:ring-pink-400"
            }
        )
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Confirm Password",
                "class": "w-full rounded-lg border border-pink-300 px-4 py-3 focus:outline-none focus:ring-2 focus:ring-pink-400"
            }
        )
    )

    class Meta:

        model = User

        fields = [ "username","first_name", "last_name", "email", "password1","password2",]


    def clean_email(self):

        email = self.cleaned_data["email"]

        if User.objects.filter(email=email).exists():

            raise forms.ValidationError(
                "Email already exists."
            )

        return email




class LoginForm(AuthenticationForm):

    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Username",
                "class": "w-full rounded-lg border border-pink-300 px-4 py-3 focus:outline-none focus:ring-2 focus:ring-pink-400"
            }
        )
    )

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "w-full rounded-lg border border-pink-300 px-4 py-3 focus:outline-none focus:ring-2 focus:ring-pink-400"
            }
        )
    )



class UserUpdateForm(forms.ModelForm):

    class Meta:

        model = User

        fields = ["first_name","last_name","email",]

        widgets = {

            "first_name": forms.TextInput(
                attrs={
                    "class":"w-full rounded-xl border px-4 py-3 focus:ring-2 focus:ring-blue-500",
                    "placeholder":"First Name"
                }
            ),

            "last_name": forms.TextInput(
                attrs={
                    "class":"w-full rounded-xl border px-4 py-3 focus:ring-2 focus:ring-blue-500",
                    "placeholder":"Last Name"
                }
            ),

            "email": forms.EmailInput(
                attrs={
                    "class":"w-full rounded-xl border px-4 py-3 focus:ring-2 focus:ring-blue-500",
                    "placeholder":"Email Address"
                }
            ),

        }


    def clean_email(self):

        email = self.cleaned_data["email"]

        qs = User.objects.filter(email=email).exclude(pk=self.instance.pk)

        if qs.exists():

            raise forms.ValidationError(
                "This email is already in use."
            )

        return email




class ProfileUpdateForm(forms.ModelForm):

    class Meta:

        model = Profile

        fields = ["profile_picture","bio","website","location","birth_date",]

        widgets = {

            "bio": forms.Textarea(
                attrs={
                    "rows":5,
                    "maxlength":300,
                    "class":"w-full rounded-xl border px-4 py-3 focus:ring-2 focus:ring-blue-500",
                    "placeholder":"Tell people about yourself..."
                }
            ),

            "website": forms.URLInput(
                attrs={
                    "class":"w-full rounded-xl border px-4 py-3 focus:ring-2 focus:ring-blue-500",
                    "placeholder":"https://example.com"
                }
            ),

            "location": forms.TextInput(
                attrs={
                    "class":"w-full rounded-xl border px-4 py-3 focus:ring-2 focus:ring-blue-500",
                    "placeholder":"Your Location"
                }
            ),

            "birth_date": forms.DateInput(
                attrs={
                    "type":"date",
                    "class":"w-full rounded-xl border px-4 py-3 focus:ring-2 focus:ring-blue-500"
                }
            ),

            "profile_picture": forms.FileInput(
                attrs={
                    "class":"hidden",
                    "accept":"image/*"
                }
            ),

        }