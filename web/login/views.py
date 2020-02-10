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
        r = ""
        text = ""
        token = ""
        if request.method == 'POST':
            form = forms.RegisterForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                ename = models.UserDetails.objects.filter(username=data['name']).exists()
                ephone = models.UserDetails.objects.filter(phone=data['phone']).exists()
                emaile = models.UserDetails.objects.filter(email=data['email']).exists()
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
                    r = requests.post('http://127.0.0.1:8000/api/token/', data=data)
                    text = r.json()
                    token = text['token']
                    #html = render(request, 'login/index.html', {'form': form, 'error': error, 'token': token})
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
                        print(data)
                        text = r.json()
                        token = text['token']
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


def dashboard(request):
    return HttpResponse("Welcome to Dashboard")