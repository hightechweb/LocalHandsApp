"""localhands URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings

from localhandsapp import views, apis

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.home, name='home'),

    # Scooper
    url(r'^scooper/sign-in/$', auth_views.login,
        {'template_name': 'scooper/sign_in.html'},
        name = 'scooper-sign-in'),
    url(r'^scooper/sign-out', auth_views.logout,
        {'next_page': '/'},
        name = 'scooper-sign-out'),
    url(r'^scooper/sign-up', views.scooper_sign_up,
        name = 'scooper-sign-up'),
    url(r'^scooper/$', views.scooper_home, name = 'scooper-home'),

    url(r'^scooper/account/$', views.scooper_account, name = 'scooper-account'),
    url(r'^scooper/task/$', views.scooper_task, name = 'scooper-task'),
    url(r'^scooper/task/add/$', views.scooper_add_task, name = 'scooper-add-task'),
    url(r'^scooper/task/edit/(?P<task_id>\d+)/$', views.scooper_edit_task, name = 'scooper-edit-task'),
    url(r'^scooper/order/$', views.scooper_order, name = 'scooper-order'),
    url(r'^scooper/report/$', views.scooper_report, name = 'scooper-report'),

    # Sign In / Sign Up / Sign Out
    url(r'^api/social/', include('rest_framework_social_oauth2.urls')),
    # /convert-token (sign_in/ sign up)
    # /revoke-token (sign_out)

    # APIS for Customers
    url(r'^api/customer/scoopers/$', apis.customer_get_scoopers),
    url(r'^api/customer/tasks/(?P<scooper_id>\d+)/$', apis.customer_get_tasks),
    url(r'^api/customer/order/add/$', apis.customer_add_order),
    url(r'^api/customer/order/latest/$', apis.customer_get_latest_order),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
