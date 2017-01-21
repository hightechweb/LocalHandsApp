from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from localhandsapp.forms import UserForm, ScooperForm, UserFormForEdit, TaskForm
from django.contrib.auth import authenticate, login

from django.contrib.auth.models import User
from localhandsapp.models import Task, Order, Driver

from django.db.models import Sum, Count, Case, When

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
    # Calculate revenue and number of order by current week
    from datetime import datetime, timedelta

    revenue = []
    orders = []

    # Calculate weekdays
    today = datetime.now()
    current_weekdays = [today + timedelta(days = i) for i in range(0 - today.weekday(), 7 - today.weekday())]

    for day in current_weekdays:
        delivered_orders = Order.objects.filter(
            scooper = request.user.scooper,
            status = Order.DELIVERED,
            created_at__year = day.year,
            created_at__month = day.month,
            created_at__day = day.day
        )
        revenue.append(sum(order.total for order in delivered_orders))
        orders.append(delivered_orders.count())


    # Top 3 Tasks
    top3_tasks = Task.objects.filter(scooper = request.user.scooper)\
                     .annotate(total_order = Sum('orderdetails__quantity'))\
                     .order_by("-total_order")[:3]

    task = {
        "labels": [task.name for task in top3_tasks],
        "data": [task.total_order or 0 for task in top3_tasks]
    }

    # Top 3 Drivers
    top3_drivers = Driver.objects.annotate(
        total_order = Count(
            Case (
                When(order__scooper = request.user.scooper, then = 1)
            )
        )
    ).order_by("-total_order")[:3]

    driver = {
        "labels": [driver.user.get_full_name() for driver in top3_drivers],
        "data": [driver.total_order for driver in top3_drivers]
    }

    return render(request, 'scooper/report.html', {
        "revenue": revenue,
        "orders": orders,
        "task": task,
        "driver": driver
    })

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
