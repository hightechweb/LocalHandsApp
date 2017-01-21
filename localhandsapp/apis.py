# from django.http import JsonResponse
import json

from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from oauth2_provider.models import AccessToken

from localhandsapp.models import Scooper, Task, Order, OrderDetails, Driver
from localhandsapp.serializers import ScooperSerializer, TaskSerializer, OrderSerializer

import stripe
from localhands.settings import STRIPE_API_KEY

stripe.api_key = STRIPE_API_KEY


##############
# CUSTOMERS
##############
def customer_get_scoopers(request):
    scoopers = ScooperSerializer(
        Scooper.objects.all().order_by("-id"),
        many = True,
        context = {"request": request}
    ).data

    return JsonResponse({"scoopers": scoopers})

def customer_get_tasks(request, scooper_id):
    tasks = TaskSerializer(
        Task.objects.filter(scooper_id=scooper_id).order_by("-id"),
        many=True
    ).data

    return JsonResponse({"tasks": tasks})

#def customer_add_order(request):
    #return JsonResponse({})

@csrf_exempt
def customer_add_order(request):
    """
        params:
            access_token
            scooper_id
            address
            order_details (json format), example:
                [{"task_id": 3, "quantity": 2},{"task_id": 4, "quantity": 3}]
            stripe_token

        return:
            {"status": "success"}
    """

    if request.method == "POST":
        # Get token
        access_token = AccessToken.objects.get(token = request.POST.get("access_token"),
            expires__gt = timezone.now())

        # Get profile
        customer = access_token.user.customer

        # Get STRIPE Token
        stripe_token = request.POST["stripe_token"]

        # Check whether customer has any order that is not delivered
        if Order.objects.filter(customer = customer).exclude(status = Order.DELIVERED):
            return JsonResponse({"status": "failed", "error": "Your last order must be completed."})

        # Check Address
        if not request.POST["address"]:
            return JsonResponse({"status": "failed", "error": "Address is required."})

        # Get Order Details
        order_details = json.loads(request.POST["order_details"])

        order_total = 0
        for task in order_details:
            order_total += Task.objects.get(id = task["task_id"]).price * task["quantity"]

        if len(order_details) > 0:

            # Create a stripe charge: this will charge customers card
            charge = stripe.Charge.create(
                amount = order_total * 100, # Amount in cents
                currency = "usd",
                source = stripe_token,
                description = "LocalMotive Order"
            )

            if charge.status != "failed":
                # Step 2 - Create an Order
                order = Order.objects.create(
                    customer = customer,
                    scooper_id = request.POST["scooper_id"],
                    total = order_total,
                    status = Order.PENDING,
                    address = request.POST["address"]
                )

                # Step 3 - Create Order details
                for task in order_details:
                    OrderDetails.objects.create(
                        order = order,
                        task_id = task["task_id"],
                        quantity = task["quantity"],
                        sub_total = Task.objects.get(id = task["task_id"]).price * task["quantity"]
                    )
                return JsonResponse({"status": "success"})
            else:
                return JsonResponse({"status": "failed", "error": "Failed to connect to Stripe."})

def customer_get_latest_order(request):
    access_token = AccessToken.objects.get(token = request.GET.get("access_token"),
        expires__gt = timezone.now())

    customer = access_token.user.customer
    order = OrderSerializer(Order.objects.filter(customer = customer).last()).data

    return JsonResponse({"order": order})

##############
# SCOOPER
##############
def scooper_order_notification(request, last_request_time):
    notification = Order.objects.filter(scooper = request.user.scooper,
        created_at__gt = last_request_time).count()

    # THE ABOVE IS LIKE THIS SQL QUERY: select count(*) from Orders where scooper = request.user.scooper AND created_at > last_request_time
    return JsonResponse({"notification": notification})

def customer_driver_location(request):
    access_token = AccessToken.objects.get(token = request.GET.get("access_token"), expires__gt = timezone.now())

    customer = access_token.user.customer

    # Get the driver's location related to the customers current order
    current_order = Order.objects.filter(customer=customer,status=Order.ONTHEWAY).last()
    location = current_order.driver.location

    return JsonResponse({"location": location})


##############
# DRIVERS
##############
def driver_get_ready_orders(request):
# TO DUE: access_token, only only drivers to view data
    orders = OrderSerializer(
        Order.objects.filter(status = Order.PROCESSING, driver = None).order_by("-id"),
        many = True
    ).data

    return JsonResponse({"orders": orders})

@csrf_exempt
# POST
# params: access_token, order_id
def driver_pick_order(request):

    if request.method == "POST":
        # Get token
        access_token = AccessToken.objects.get(token = request.POST.get("access_token"), expires__gt = timezone.now())

        # Get Driver
        driver = access_token.user.driver

        # Check if driver can only pick up one order at the same time
        if Order.objects.filter(driver = driver).exclude(status = Order.DELIVERED):
            return JsonResponse({"status": "failed", "error": "You can only pick one order at the same time."})

        try:
            order = Order.objects.get(
                id = request.POST["order_id"],
                driver = None,
                status = Order.PROCESSING
            )
            order.driver = driver
            order.status = Order.ONTHEWAY
            order.picked_at = timezone.now()
            order.save()

            return JsonResponse({"status": "success"})

        except Order.DoesNotExist:
            return JsonResponse({"status": "failed", "error": "This order has been picked up by another."})

    return JsonResponse({})

# GET params: access_token
def driver_get_latest_order(request):
    # Get token
    access_token = AccessToken.objects.get(token = request.GET.get("access_token"), expires__gt = timezone.now())

    driver = access_token.user.driver
    order = OrderSerializer(
        Order.objects.filter(driver = driver).order_by("picked_at").last()
    ).data

    return JsonResponse({"order": order})

# POST params: access_token, order_id
@csrf_exempt
def driver_complete_order(request):
    # Get token
    access_token = AccessToken.objects.get(token = request.POST.get("access_token"), expires__gt = timezone.now())

    driver = access_token.user.driver

    order = Order.objects.get(id = request.POST["order_id"], driver = driver)
    order.status = Order.DELIVERED
    order.delivered_at = timezone.now()
    order.save()

    return JsonResponse({"status": "success"})

# GET params: access_token
def driver_get_revenue(request):
    access_token = AccessToken.objects.get(token = request.GET.get("access_token"), expires__gt = timezone.now())

    driver = access_token.user.driver

    from datetime import timedelta

    revenue = {}
    today = timezone.now()
    current_weekdays = [today + timedelta(days = i) for i in range(0 - today.weekday(), 7 - today.weekday())]

    for day in current_weekdays:
        orders = Order.objects.filter(
            driver = driver,
            status = Order.DELIVERED,
            created_at__year = day.year,
            created_at__month = day.month,
            created_at__day = day.day
        )

        revenue[day.strftime("%a")] = sum(order.total for order in orders)

    return JsonResponse({"revenue": revenue})

# POST: params: access_token, "lat,lng"
@csrf_exempt
def driver_update_location(request):
    if request.method == "POST":
        access_token = AccessToken.objects.get(token = request.POST.get("access_token"), expires__gt = timezone.now())

        driver = access_token.user.driver

        # SET locations string => database
        driver.location = request.POST["location"]
        driver.save()

        return JsonResponse({"status": "success"})
