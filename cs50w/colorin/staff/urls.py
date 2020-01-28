from django.urls import path
from . import views

urlpatterns = [
	path("staffboard", views.staffboard, name="staffboard"),
	path("staffapprovetheme", views.staffapprovetheme, name="staffapprovetheme"),
	path("staffapproveplatform", views.staffapproveplatform, name="staffapproveplatform"),
	path("staffreport", views.staffreport, name="staffreport"),
	path("reporteditem/<str:ctype>/<str:fid>/<str:cid>/", views.reporteditem, name="reporteditem"),
	path("resolvereported/<str:ctype>/<str:fid>/<str:cid>/", views.resolvereported, name="resolvereported"),
	path("memberinfo/<str:ctype>/<str:cid>/", views.memberinfo, name="memberinfo"),
	path("profileinfo/<str:cid>/", views.profileinfo, name="profileinfo")
]
