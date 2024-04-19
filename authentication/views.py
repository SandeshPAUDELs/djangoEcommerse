
import random
from django.contrib import messages
from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.conf import settings



def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if not email:
            messages.error(request, 'Email is required')
            return redirect('register')

        if password1 != password2:
            messages.error(request, 'Passwords do not match')
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return redirect('register')
        else:
            user = User.objects.create_user(username=username, email=email, password=password1)
            user.save()
            messages.success(request, 'Account created successfully')
            user = authenticate(username=username, password=password1)
            if user is not None:
                login(request, user)
            return redirect('home')

    else:
        return render(request, 'register.html')
    
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username OR password is incorrect')

    return render(request, 'login.html')

    
def logoutUser(request):
    logout(request)
    return redirect('home')




otps = {}


def send_otp(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        
        # Check if the email exists in the User model
        if User.objects.filter(email=email).exists():
            otp = random.randint(1000, 9999)
            otps[email] = otp
            send_mail('OTP Verification', f'Your OTP is {otp}', 'paudelsandesh181@gmail.com', [email], fail_silently=False,)
            print(f'OTP sent to {email} is {otp}')
            return redirect('verify_otp')
        else:
            # If the email does not exist, add an error message and redirect back to 'send_otp'
            messages.error(request, 'This email does not exist')
            return redirect('send_otp')
    else:
        return render(request, 'send_otp.html')
    

    
    
def verify_otp(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        otp = request.POST.get('otp')
        if otps.get(email) == int(otp):
            return redirect('forget_password')
        else:
            messages.error(request, 'Invalid OTP')
            return render(request, 'verify_otp.html')  # Render the same page with error message
    else:
        return render(request, 'verify_otp.html')


def forget_password(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = User.objects.get(email=email)
        user.set_password(password)
        user.save()
        messages.success(request, 'Password changed successfully')
        return redirect('loginPage')
    else:
        return render(request, 'forget_password.html')