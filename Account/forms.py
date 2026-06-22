from django import forms
from django.contrib.auth.models import User 
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


class RegistrationForm(UserCreationForm):
    username = forms.CharField(
         widget=forms.TextInput(
             attrs={
                 "placeholder": "Username",
                 "class": "w-full px-3 py-1 border border-pink-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-pink-300"
             }
         )
    )

    email = forms.EmailField( 

        widget=forms.EmailInput(
             attrs={
                 "placeholder": "Email",
                 "class": "w-full px-3 py-1 border border-pink-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-pink-300"
             }
         )
    )

    first_name = forms.CharField(
         widget=forms.TextInput(
             attrs={
                 "placeholder": "First name",
                 "class": "w-full px-3 py-1 border border-pink-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-pink-300"
             }
         )
    )

    last_name = forms.CharField(
         widget=forms.TextInput(
             attrs={
                 "placeholder": "Last name",
                 "class": "w-full px-3 py-1 border border-pink-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-pink-300"
             }
         )
    )

    password1 = forms.CharField(
         label="Password",
         widget=forms.PasswordInput(
             attrs={
                 "placeholder": "Password",
                 "class": "w-full px-3 py-1 border border-pink-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-pink-300"
             }
         )
    )

    password2 = forms.CharField(
         label="Confirm Password",
         widget=forms.PasswordInput(
             attrs={
                 "placeholder": "Confirm password",
                 "class": "w-full px-3 py-1 border border-pink-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-pink-300"
             }
         )
    )

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email"]

        





class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Username",
        widget=forms.TextInput(
            attrs={
                 "placeholder": "Username or Email",
                 "class": "w-full px-3 py-1 border border-pink-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-pink-500"
             }
         )
     )

    password = forms.CharField(
         label="Password",
         widget=forms.PasswordInput(
             attrs={
                 "placeholder": "password",
                 "class": "w-full px-3 py-1 border border-pink-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-pink-300"
             }
         )
    )

    class Meta:
        model = User
        fields = ["username","password"]

