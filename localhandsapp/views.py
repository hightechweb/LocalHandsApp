from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from localhandsapp.forms import UserForm, ScooperForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

# Create your views here.
def home(request):
    # return render(request, 'home.html', {})
    return redirect(scooper_home)

@login_required(login_url='/scooper/sign-in/')
def scooper_home(request):
    return render(request, 'scooper/home.html', {})

def scooper_sign_up(request):
    user_form = UserForm()
    scooper_form = ScooperForm()

    if request.method == "POST":
        user_form = UserForm(request.POST)
        scooper_form = ScooperForm(request.POST, request.FILES)

        if user_form.is_valid() and scooper_form.is_valid():
            new_user = User.objects.create_user(**user_form.cleaned_data)
            new_scooper = scooper_form.save(commit=False)
            new_scooper.user = new_user
            new_scooper.save()

            login(request, authenticate(
                username = user_form.cleaned_data["username"],
                password = user_form.cleaned_data["password"]
            ))

            return redirect(scooper_home)

    return render(request, 'scooper/sign_up.html', {
        "user_form": user_form,
        "scooper_form": scooper_form
    })
