from django import forms


class RegisterForm(forms.Form):
    name = forms.CharField(label="Name",max_length=50, widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    phone  = forms.CharField(label="Phone Number", max_length = 13, widget=forms.TextInput(attrs={'placeholder': 'Phone Number'}))
    email = forms.EmailField(label="Email Address", max_length=50, widget=forms.TextInput(attrs={'placeholder': 'Email Address'}))
    password = forms.CharField(label="Password", max_length=13, widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    password2 = forms.CharField(label="Confirm Password", max_length=50, widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Passsword'}))

class LoginForm(forms.Form):
    name = forms.CharField(label="Name",max_length=50, widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(label="Name", max_length=50, widget=forms.TextInput(attrs={'placeholder': 'Password'}))