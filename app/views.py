from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from login import settings
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.models import auth
from . tokens import generate_token

# Create your views here.
def home(request):
    return render(request, "index.html")

def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        #fname = request.POST['fname']
        #lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['psw']
        pass2 = request.POST['psw-repeat']
        
        if User.objects.filter(username=username):
            messages.error(request, "Username already exist! Please try some other username.")
            return redirect('home')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email Already Registered!!")
            return redirect('home')
        
        if len(username)>20:
            messages.error(request, "Username must be under 20 charcters!!")
            return redirect('home')
        
        if pass1 != pass2:
            messages.error(request, "Passwords didn't matched!!")
            return redirect('home')
        
        if not username.isalnum():
            messages.error(request, "Username must be Alpha-Numeric!!")
            return redirect('home')
        
        myuser = User.objects.create_user(username, email, pass1)
        #myuser.first_name = fname
        #myuser.last_name = lname
        myuser.email = email
        myuser.username = username
        #myuser.is_active = False
        myuser.is_active = True
        myuser.save()
        messages.success(request, "Your Account has been created succesfully!!" )
        return redirect('signin')
     
    return render(request, "signup.html")



def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['psw']
        
        user = authenticate(username=username, password=pass1)
        
        if user is not None:
            if user.is_active:
                login(request, user)
            # fname = user.first_name
                messages.success(request, "Logged In Sucessfully!!")
                return render(request, "index.html")
        else:
            messages.error(request, "Bad Credentials!!")
            return redirect('home')
    
    return render(request, "signin.html")



def signout(request):
    logout(request)
    messages.success(request, "Logged Out Successfully!!")
    return render(request, "index.html")

    