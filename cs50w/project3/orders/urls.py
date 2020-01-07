from django.urls import path

from . import views

urlpatterns = [ 
    path("", views.home, name="home"),
    path("mylogin", views.mylogin, name="mylogin"),
    path("mylogout", views.mylogout, name="mylogout"),
    path("mysignup", views.mysignup, name="mysignup"),
    path("clientboard", views.clientboard, name="clientboard"),
    path("staffboard", views.staffboard, name="staffboard"),
    path("neworder", views.neworder, name="neworder"),
    path("clientorderlist", views.clientorderlist, name="clientorderlist"),
    path("stafforderlist", views.stafforderlist, name="stafforderlist"),
    path("stafforderstatus", views.stafforderstatus, name="stafforderstatus")
]

