from django.contrib import admin
# from .models import Member, Theme, Platform, Network, Suggestion, Comment, Message, Flag
from .models import *

admin.site.register(Member)
admin.site.register(Theme)
admin.site.register(Platform)
admin.site.register(Network)
admin.site.register(Suggestion)
admin.site.register(Comment)
admin.site.register(Message)
admin.site.register(Flag)
