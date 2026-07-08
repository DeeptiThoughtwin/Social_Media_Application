from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Profile
import re



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
        label=" Password",
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "w-full rounded-lg border border-pink-300 px-4 py-3 focus:outline-none focus:ring-2 focus:ring-pink-400"
            }
        )
    )

    password2 = forms.CharField(
        label="Confirm Password",
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




    def clean_username(self):
        username = self.cleaned_data["username"].strip()

        if not username:
            raise forms.ValidationError("Username is required.")

        if username[0].isdigit():
            raise forms.ValidationError(
                "Username cannot start with a number."
            )

        if len(username) < 4:
            raise forms.ValidationError(
                "Username must be at least 4 characters."
            )

        if len(username) > 20:
            raise forms.ValidationError(
                "Username cannot be more than 20 characters."
            )

        if not re.fullmatch(r"[A-Za-z][A-Za-z0-9_]*", username):
            raise forms.ValidationError(
                "Username can contain only letters, numbers, and underscores."
            )

        if User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError(
                "Username already exists."
            )
        
        if not re.search(r"[A-Z]", username):
            raise forms.ValidationError(
        "Username must contain at least one uppercase letter."
        )

        if not re.search(r"[a-z]", username):
            raise forms.ValidationError(
                "Username must contain at least one lowercase letter."
            )

        return username

    

    def clean_first_name(self):
        first_name = self.cleaned_data["first_name"].strip()

        if not first_name:
            raise forms.ValidationError("First name is required.")

        if len(first_name) < 2:
            raise forms.ValidationError(
                "First name must be at least 2 characters."
            )

        if first_name[0].isdigit():
            raise forms.ValidationError(
                "First name cannot start with a number."
            )

        if not re.fullmatch(r"[A-Za-z\s'-]+", first_name):
            raise forms.ValidationError(
                "First name should contain only letters."
            )

        return first_name.title()

   

    def clean_last_name(self):
        last_name = self.cleaned_data["last_name"].strip()

        if not last_name:
            raise forms.ValidationError("Last name is required.")

        if len(last_name) < 2:
            raise forms.ValidationError(
                "Last name must be at least 2 characters."
            )

        if last_name[0].isdigit():
            raise forms.ValidationError(
                "Last name cannot start with a number."
            )

        if not re.fullmatch(r"[A-Za-z\s'-]+", last_name):
            raise forms.ValidationError(
                "Last name should contain only letters."
            )

        return last_name.title()

    

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()

        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(
                "This email is already registered."
            )

        return email

  

    def clean_password1(self):
        password = self.cleaned_data["password1"]

        if len(password) < 8:
            raise forms.ValidationError(
                "Password must be at least 8 characters."
            )

        if not re.search(r"[A-Z]", password):
            raise forms.ValidationError(
                "Password must contain at least one uppercase letter."
            )

        if not re.search(r"[a-z]", password):
            raise forms.ValidationError(
                "Password must contain at least one lowercase letter."
            )

        if not re.search(r"\d", password):
            raise forms.ValidationError(
                "Password must contain at least one number."
            )

        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            raise forms.ValidationError(
                "Password must contain at least one special character."
            )

        return password



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



