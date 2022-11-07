from django.shortcuts import redirect, render
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib import messages,auth
from register.models import Student

# Create your views here.
def loginUser(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, 'you are logged in')
            return redirect('dashboard')
        else:
            messages.warning(request, 'invalid credentials')
            return redirect('login')
    return render(request,'login.html')

def registerUser(request):
    if request.method == 'POST':
        username =request.POST['username']
        password =request.POST['password']
        email = request.POST['email']
        confirm_password =request.POST['confirm_password']
        name = request.POST['name']
        user = User.objects.create_user(username=username,email=email,password = password)
        user.save()
        studentusr = Student(name = name,dob='2000-12-12',studentUser = user)
        studentusr.save()
        messages.success(request,"Registerd successfully")
        return redirect('loginUser')
    return render(request,'register.html')

def logoutUser(request):
    logout(request)
    return redirect('loginUser')
