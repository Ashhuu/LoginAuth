from django.shortcuts import render, redirect
from django.http import HttpResponse
import requests
from . import forms
from . import models

# Create your views here.


def home(request):
    url = "http://127.0.0.1:8000/api-token-auth/"

    querystring = {"username": "ashhuu27", "password": "112233"}

    headers = {
        'x-rapidapi-host': "gurubrahma-smsly-sms-to-india-v1.p.rapidapi.com",
        'x-rapidapi-key': "0f613269e2msh5fc467929a8d0edp11181ejsn5fb72d7062f1"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    print(response.text)
    return HttpResponse("Hello")

def register(request):
    if request.COOKIES.get('token'):
        tokenConfirm = request.COOKIES.get('token')
        return redirect('Dashboard')
    else:
        error = ""
        token = ""
        if request.method == 'POST':
            form = forms.RegisterForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                ename = models.UserDetails.objects.filter(username=data['name']).exists()
                ephone = models.UserDetails.objects.filter(phone=data['phone']).exists()
                emaile = models.UserDetails.objects.filter(email=data['email']).exists()
                # Basic Form Validations
                if data['password'] != data['password2']:
                    error = "Password did not match"
                elif ename == True:
                    error = "The username is already registered"
                elif ephone == True:
                    error = "Number already registered, please enter another number"
                elif emaile == True:
                    error = "The email is already registered"
                elif len(data['phone']) != 10:
                    error = "The phone number should be of 10 digits"
                else:
                    # Requesting API To create user and return token
                    r = requests.post('http://127.0.0.1:8000/api/token/', data=data)
                    text = r.json()
                    token = text['token']
                    # Adding Token to UserDetails
                    query = models.UserDetails.objects.get(username=data['name'])
                    query.token = token
                    query.save()
                    # Setting Redirect and adding token to cookies
                    html = redirect('Dashboard')
                    html.set_cookie('token', token)
                    return html

        else:
            form = forms.RegisterForm()
    return render(request, 'login/index.html', {'form': form, 'error': error, 'token': token})

def login(request):
    if request.COOKIES.get('token'):
        tokenConfirm = request.COOKIES.get('token')
        return redirect('Dashboard')
    else:
        error = ""
        if request.method == 'POST':
            form = forms.LoginForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                checkUser = models.UserDetails.objects.filter(username=data['name']).exists()
                if checkUser == True:
                    query = models.UserDetails.objects.filter(username=data['name']).values()
                    row = query[0]
                    if row['password'] == data['password']:
                        r = requests.post('http://127.0.0.1:8000/api/gentoken/', data=data)
                        text = r.json()
                        token = text['token']
                        query = models.UserDetails.objects.get(username=data['name'])
                        query.token = token
                        query.save()
                        #html = render(request, 'login/login.html', {'form': form, 'error': error})
                        html = redirect('Dashboard')
                        html.set_cookie('token', token)
                        return html
                    else:
                        error = "Username and password does not match"
                else:
                    error = "The user does not exist"

        else:
            form = forms.LoginForm()
    return render(request, 'login/login.html', {'form': form, 'error': error})

def logout(request):
    if request.COOKIES.get('token'):
        token = request.COOKIES.get('token')
        html = redirect('Login')
        html.delete_cookie('token')
        r = requests.post('http://127.0.0.1:8000/api/verify/', data={'token': token})
        text = r.json()
        check = text['exists']
        if check == 'true':
            print("Successfully Deleted Cookies and Logged out")
        elif check == 'false':
            print("Could not find verified token")
        return html
    else:
        print("Could not find any token")
        return redirect('Login')


def dashboard(request):
    if request.COOKIES.get('token'):
        tokenConfirm = request.COOKIES.get('token')
        r = requests.post('http://127.0.0.1:8000/api/verify/', data={'token': tokenConfirm})
        text = r.json()
        check = text['exists']
        if check == 'true':
            print("Successfully Deleted Cookies and Logged out")
            details = models.UserDetails.objects.get(token=tokenConfirm)
            user = details.username
            email = details.email
        elif check == 'false':
            redirect('404')
        print(check)
    else:
        return redirect('404')
    return render(request, 'login/dashboard.html', {'user':user, 'email':email})

def error404(request):
    return render(request, 'login/404.html', {})