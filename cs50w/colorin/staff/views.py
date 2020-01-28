import json
from datetime import datetime
from django.shortcuts import render
from members.models import MemberStatus, ThemeStatus, PlatformStatus, NetworkStatus, SuggestionStatus, CommentStatus, MessageStatus, FlagStatus, ItemType
from members.models import Member, Platform, Network, Theme, Suggestion, Comment, Message, Flag
from django.http import HttpResponseRedirect, HttpResponseBadRequest, HttpResponseNotAllowed, HttpResponseForbidden, HttpResponseNotFound, HttpResponseServerError, JsonResponse
from django.contrib.auth.models import User
from django.urls import reverse
from django.db import IntegrityError
from members.helpers import *


def staffboard(request):
    if request.user.is_staff == False:
        return HttpResponseForbidden("Access not allowed!")
    if request.method != "GET":
        return HttpResponseNotAllowed(["GET"])

    prit = Theme.objects.filter(status=ThemeStatus.PRIVATE).order_by("name")
    prip = Platform.objects.filter(status=PlatformStatus.PRIVATE).order_by("url")
    pris = Network.objects.filter(status=NetworkStatus.PRIVATE).order_by("url")
    return render(request, "staff/staffboard.html", {"prithemes": prit, "priplts": prip, "prisocs":pris})


def staffapprovetheme(request):
    if request.user.is_staff == False:
        return HttpResponseForbidden("Access not allowed!")
    if (request.method != "POST"):
        return HttpResponseNotAllowed(["POST"])
    
    ntx = 0
    cid = request.POST["cid"]
    if len(cid) < 1 or len(cid) > 18:
        ntx += 1
    status = request.POST["status"]
    if len(status) < 2 or len(status) > 10 or status not in ["public", "archived"]:
        ntx += 1
    name = request.POST["name"]
    if len(name) < 2 or len(name) > 80:
        ntx += 1
    if (ntx > 0):
        return HttpResponseBadRequest("Incorrect parameter!")

    tx = ""
    name = name.capitalize()
    theme = getTheme(name = name)
    if theme is not None and str(theme.id) != cid:
        tx = tx + "Theme name is duplicate; "
    theme = getiTheme(id=cid)
    if theme is None:
        tx = tx + "Theme id not found; "
    else:
        if theme.status != ThemeStatus.PRIVATE:
            tx = tx + "status is not private; "
    if (len(tx) > 0):
        return JsonResponse({"error":"yes", "message":tx})
    # update    
    try:
        theme.name = name
        if status == "public":
            theme.status = ThemeStatus.PUBLIC
        else:
            theme.status = ThemeStatus.ARCHIVED
        theme.save()
    except Exception as exc:
        return JsonResponse({"error":"yes", "message":str(exc)})               
    return JsonResponse({"error":"no", "message":"ok"})


def staffapproveplatform(request):
    if request.user.is_staff == False:
        return HttpResponseForbidden("Access not allowed!")
    if (request.method != "POST"):
        return HttpResponseNotAllowed(["POST"])
    
    ntx = 0
    cid = request.POST["cid"]
    if len(cid) < 1 or len(cid) > 18:
        ntx += 1
    status = request.POST["status"]
    if len(status) < 2 or len(status) > 10 or status not in ["public", "archived"]:
        ntx += 1
    type = request.POST["type"]
    if len(type) < 1 or len(type) > 10 or type not in ["social", "resource"]:
        ntx += 1
    name = request.POST["name"]
    if len(name) < 2 or len(name) > 80:
        ntx += 1
    if (ntx > 0):
        return HttpResponseBadRequest("Incorrect parameter!")

    tx = ""
    name = name.lower()
    rs = carveUrl(name)
    name = rs[0]
    tx = tx + rs[1] 
    if type == "resource":
        plt = getPlatform(url = name)
        if plt is not None and str(plt.id) != cid:
            tx = tx + "Platform URL is duplicate; "    
        plt = getiPlatform(id=cid)
        if plt is None:
            tx = tx + "Platform not found; "
        else:
            if plt.status != PlatformStatus.PRIVATE:
                tx = tx + "status is not private; "
        if (len(tx) > 0):
            return JsonResponse({"error":"yes", "message":tx})
        try:
            plt.url = name
            if status == "public":
                plt.status = PlatformStatus.PUBLIC
            else:
                plt.status = PlatformStatus.ARCHIVED
            plt.save()
        except Exception as exc:
            return JsonResponse({"error":"yes", "message":str(exc)})               
    elif type == "social":
        soc = getNetwork(url = name)
        if soc is not None and str(soc.id) != cid:
            tx = tx + "social network URL is duplicate; "    
        soc = getiNetwork(id=cid)
        if soc is None:
            tx = tx + "social network not found; "
        else:
            if soc.status != NetworkStatus.PRIVATE:
                tx = tx + "status is not private; "
        if (len(tx) > 0):
            return JsonResponse({"error":"yes", "message":tx})
        try:
            soc.url = name
            if status == "public":
                soc.status = NetworkStatus.PUBLIC
            else:
                soc.status = NetworkStatus.ARCHIVED
            soc.save()
        except Exception as exc:
            return JsonResponse({"error":"yes", "message":str(exc)})               

    return JsonResponse({"error":"no", "message":"ok"})


def staffreport(request):
    if request.user.is_staff == False:
        return HttpResponseForbidden("Access not allowed!")
    if request.method != "GET":
        return HttpResponseNotAllowed(["GET"])

    flags = Flag.objects.filter(status=FlagStatus.INITIATED)
    return render(request, "staff/staffreport.html", {"flags":flags})


def reporteditem(request, ctype, fid, cid):
    if request.user.is_staff == False:
        return HttpResponseForbidden("Access not allowed!")
    if request.method != "GET":
        return HttpResponseNotAllowed(["GET"])    
    if len(fid) > 18 or len(cid) > 18 or len(ctype) > 2 or ctype not in ["1", "2", "3", "4"]:
        return HttpResponseBadRequest("Incorrect parameter!")
    ntype = int(ctype)
    tx = ""

    if ntype == ItemType.SUGGESTION:
        sugg = getiSuggestion(cid)
        if sugg is None:
            tx = "Suggestion not found!"
        else:
            return render(request, 'staff/reportedsuggestion.html', {"ctype":ctype, "fid":fid, "elem":sugg})
    elif ntype == ItemType.COMMENT:
        cmnt = getiComment(cid)
        if cmnt is None:
            tx = "Comment not found!"
        else:
            return render(request, 'staff/reportedcomment.html', {"ctype":ctype, "fid":fid, "elem":cmnt})
    elif ntype == ItemType.MESSAGE:
        prime = getiMessage(cid)
        if prime is None:
            tx = "Private message not found!"
        else:
            return render(request, 'staff/reportedmessage.html', {"ctype":ctype, "fid":fid, "elem":prime})
    elif ntype == ItemType.PROFILE:
        opro = getiMember(cid)
        if opro is None:
            tx = "Profile not found!"
        else:
            return render(request, "staff/reportedprofile.html", {"ctype":ctype, "fid":fid, "gobuddy":opro})
    # we get here if the reported item is gone
    oflag = getiFlag(fid)
    if oflag is not None:
        try:
            oflag.status = FlagStatus.PROCESSED
            oflag.save()
        except Exception as exc:
            return HttpResponseServerError("The item was not found and something went wrong while processing the report!")    
            
    return HttpResponseNotFound("The item was not found and the report has been set as 'Processed'!")


def resolvereported(request, ctype, fid, cid):
    if request.user.is_staff == False:
        return HttpResponseForbidden("Access not allowed!")
    if request.method != "GET":
        return HttpResponseNotAllowed(["GET"])    
    if len(fid) > 18 or len(cid) > 18 or len(ctype) > 2 or ctype not in ["1", "2", "3", "4"]:
        return HttpResponseBadRequest("Incorrect parameter!")
    ntype = int(ctype)
    
    if cid != "0":
        if ntype == ItemType.SUGGESTION:
            osug = getiSuggestion(cid)
            if osug is not None and osug.status == SuggestionStatus.PUBLIC:
                try:
                    osug.status = SuggestionStatus.ARCHIVED
                    osug.save()
                except Exception as exc:
                    return HttpResponseServerError("Something went wrong while archiving the suggestion!")
        elif ntype == ItemType.COMMENT:
            ocom = getiComment(cid)
            if ocom is not None and ocom.status == CommentStatus.PUBLIC:
                try:
                    ocom.status = CommentStatus.ARCHIVED
                    ocom.save()
                except Exception as exc:
                    return HttpResponseServerError("Something went wrong while archiving the comment!")
        elif ntype == ItemType.MESSAGE:
            omes = getiMessage(cid)
            if omes is not None and omes.status == MessageStatus.PRIVATE:
                try:
                    omes.status = MessageStatus.ARCHIVED
                    omes.save()
                except Exception as exc:
                    return HttpResponseServerError("Something went wrong while archiving the private message!")
        elif ntype == ItemType.PROFILE:
            omem = getiMember(cid)
            if omem is not None and omem.status == MemberStatus.PUBLIC:
                try:
                    omem.status = MemberStatus.PRIVATE
                    omem.save()
                except Exception as exc:
                    return HttpResponseServerError("Something went wrong while turning private the member profile!")

    oflag = getiFlag(fid)
    if oflag is not None and oflag.status == FlagStatus.INITIATED:
        try:
            if cid == "0":
                oflag.status = FlagStatus.ARCHIVED
            else:
                oflag.status = FlagStatus.PROCESSED
            oflag.save()
        except Exception as exc:
            return HttpResponseServerError("Something went wrong while updating the report table!")

    return HttpResponseRedirect(reverse("staffreport"))


def memberinfo(request, ctype, cid):
    if request.user.is_staff == False:
        return HttpResponseForbidden("Access not allowed!")
    if (request.method != "GET"):
        return HttpResponseNotAllowed(["GET"])
    if len(cid) > 18 or len(ctype) > 2 or ctype not in ["1", "2", "5"]:
        return HttpResponseBadRequest("Incorrect parameter!")
    ntype = int(ctype)   
    
    gobuddy = getiMember(cid)
    if gobuddy is None:
        return HttpResponseNotFound("Member not found!")    

    if ntype == ItemType.SUGGESTION:
        golist = gobuddy.member_suggestions.order_by("-id")
        return render(request, "staff/membersuggestions.html", {"ctype":ctype, "gobuddy":gobuddy, "golist":golist})
    elif ntype == ItemType.COMMENT:
        golist = gobuddy.member_comments.order_by("-id")
        return render(request, "staff/membercomments.html", {"ctype":ctype, "gobuddy":gobuddy, "golist":golist})
    elif ntype == ItemType.REPORT:
        golist = gobuddy.member_flags.order_by("-id")
        return render(request, "staff/memberreports.html", {"ctype":ctype, "gobuddy":gobuddy, "golist":golist})


def profileinfo(request, cid):
    if request.user.is_staff == False:
        return HttpResponseForbidden("Access not allowed!")
    if (request.method != "GET"):
        return HttpResponseNotAllowed(["GET"])
    if len(cid) > 18:
        return HttpResponseBadRequest("Incorrect parameter!")
    
    gobuddy = getiMember(cid)
    if gobuddy is None:
        return HttpResponseNotFound("Member not found!")    
    return render(request, "staff/profileinfo.html", {"gobuddy":gobuddy})
