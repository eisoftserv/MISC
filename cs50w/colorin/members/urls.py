from django.urls import path
from . import views

urlpatterns = [
	path("", views.index, name="index"),
	path("themedetails/<str:cid>/", views.themedetails, name="themedetails"),
	path("suggestionrecord", views.suggestionrecord, name="suggestionrecord"),
	path("itemdelete", views.itemdelete, name="itemdelete"),
	path("mylogin", views.mylogin, name="mylogin"),
	path("mylogout", views.mylogout, name="mylogout"),
	path("mysignup", views.mysignup, name="mysignup"),
	path("memberboard", views.memberboard, name="memberboard"),
	path("platformlist", views.platformlist, name="platformlist"),
	path("platformdetails/<str:cid>/", views.platformdetails, name="platformdetails"),
	path("memberprofile", views.memberprofile, name="memberprofile"),
	path("cancel_memberprofile", views.cancel_memberprofile, name="cancel_memberprofile"),
	path("membernewtheme", views.membernewtheme, name="membernewtheme"),
	path("membernewplatform", views.membernewplatform, name="membernewplatform"),
	path("commentlist/<str:ctype>/<str:oid>/<str:cid>/", views.commentlist, name="commentlist"),
	path("commentrecord", views.commentrecord, name="commentrecord"),
	path("itemflag", views.itemflag, name="itemflag"),
	path("memberdetails/<str:cid>/", views.memberdetails, name="memberdetails"),
	path("incominglist", views.incominglist, name="incominglist"),
	path("outgoinglist", views.outgoinglist, name="outgoinglist"),
	path("privatemessage", views.privatemessage, name="privatemessage")
]
