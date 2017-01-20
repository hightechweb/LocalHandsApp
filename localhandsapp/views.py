from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from localhandsapp.forms import UserForm, ScooperForm, UserFormForEdit, TaskForm
from django.contrib.auth import authenticate, login

from django.contrib.auth.models import User
from localhandsapp.models import Task, Order

# Create your views here.
def home(request):
    # return render(request, 'home.html', {})
    return redirect(scooper_home)

@login_required(login_url='/scooper/sign-in/')
def scooper_home(request):
    # return render(request, 'scooper/home.html', {})
    return redirect(scooper_order)

@login_required(login_url='/scooper/sign-in/')
def scooper_account(request):
    user_form = UserFormForEdit(instance = request.user)
    scooper_form = ScooperForm(instance = request.user.scooper)

    if request.method == "POST":
        user_form = UserFormForEdit(request.POST, instance = request.user)
        scooper_form = ScooperForm(request.POST, request.FILES, instance = request.user.scooper)

        if user_form.is_valid() and scooper_form.is_valid():
            user_form.save()
            scooper_form.save()

    return render(request, 'scooper/account.html', {
        "user_form": user_form,
        "scooper_form": scooper_form
    })

@login_required(login_url='/scooper/sign-in/')
def scooper_task(request):
    task = Task.objects.filter(scooper = request.user.scooper).order_by("-id")
    return render(request, 'scooper/task.html', {"tasks": task})

@login_required(login_url='/scooper/sign-in/')
def scooper_add_task(request):
    form = TaskForm()

    if request.method == "POST":
        form = TaskForm(request.POST)

        if form.is_valid():
            task = form.save(commit=False)
            task.scooper = request.user.scooper
            task.save()
            return redirect(scooper_task)

    return render(request, 'scooper/add_task.html', {
        "form": form
    })

@login_required(login_url='/scooper/sign-in/')
def scooper_edit_task(request, task_id):
    form = TaskForm(instance=Task.objects.get(id = task_id))

    if request.method == "POST":
        form = TaskForm(request.POST, instance= Task.objects.get(id = task_id))

        if form.is_valid():
            form.save()
            return redirect(scooper_task)

    return render(request, 'scooper/edit_task.html', {
        "form": form
    })

@login_required(login_url='/scooper/sign-in/')
def scooper_order(request):
    if request.method == "POST":
        order = Order.objects.get(id = request.POST["id"], scooper = request.user.scooper)

        if order.status == Order.PENDING:
            order.status = Order.PROCESSING
            order.save()

    orders = Order.objects.filter(scooper=request.user.scooper).order_by("-id")
    return render(request, 'scooper/order.html', {"orders": orders})

@login_required(login_url='/scooper/sign-in/')
def scooper_report(request):
    return render(request, 'scooper/report.html', {})

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
