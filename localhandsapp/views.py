from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    # return render(request, 'home.html', {})
    return redirect(scooper_home)

@login_required(login_url='/scooper/sign-in/')
def scooper_home(request):
    return render(request, 'scooper/home.html')
