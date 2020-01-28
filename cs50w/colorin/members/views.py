import json
from datetime import datetime
from django.shortcuts import render
from .models import MemberStatus, ThemeStatus, PlatformStatus, NetworkStatus, FlagStatus, ItemType, CommentStatus, SuggestionStatus, MessageStatus
from .models import Member, Platform, Network, Theme, Suggestion, Comment, Message, Flag
from django.http import HttpResponseRedirect, HttpResponseBadRequest, HttpResponseNotAllowed, HttpResponseForbidden, HttpResponseNotFound, HttpResponseGone, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.urls import reverse
from django.db import IntegrityError
from .helpers import *


def memberboard(request):
    if request.method != "GET":
        return HttpResponseNotAllowed(["GET"])
    pubt = Theme.objects.filter(status=ThemeStatus.PUBLIC).order_by("name")
    return render(request, "members/memberboard.html", {"pubthemes": pubt})


def platformlist(request):
    if request.method != "GET":
        return HttpResponseNotAllowed(["GET"])
    pubp = Platform.objects.filter(status=PlatformStatus.PUBLIC).order_by("url")
    return render(request, "members/platformlist.html", {"pubplts":pubp})


def index(request):
    if request.method != "GET":
        return HttpResponseNotAllowed(["GET"])
    if (request.user is None or request.user.is_authenticated == False):
        return HttpResponseRedirect(reverse("mylogin"))
    if request.user.is_staff:
       return HttpResponseRedirect(reverse("staffboard"))
    return HttpResponseRedirect(reverse("memberboard"))


def mylogin(request):
    if (request.method == "GET"):
        return render(request, "members/mylogin.html", {"message":""})
    if (request.method != "POST"):
        return HttpResponseNotAllowed(["GET", "POST"])    
    
    user = request.POST["username"]
    pwd = request.POST["password"]
    if (len(user)>240 or len(pwd)>240):
        return HttpResponseBadRequest("Incorrect value(s)!")

    tx = ""
    if (len(user)<6 or len(pwd)<6):
        tx = tx + "User name and password need to have at least 6 characters; "
    if (len(user)>50 or len(pwd)>50):
        tx = tx + "User name and password are limited to maximum 50 characters!"
    if len(tx) > 0:
        return render(request, "members/mylogin.html", {"message":tx})

    try:
        resp = authenticate(request, username = user, password = pwd)
        if (resp):
            login(request, resp)
            if request.user.is_staff:
                return HttpResponseRedirect(reverse("staffboard"))

            nstatus = getMemberStatus(resp.username)
            if (nstatus is None or nstatus == MemberStatus.ARCHIVED):
                logout(request)
                return render(request, "members/mylogin.html", {"message":"Member not accessible!"})
        else:
            return render(request, "members/mylogin.html", {"message":"The login has failed!"})
    except Exception as exc:
        return render(request, "members/mylogin.html", {"message":"The authentication has failed: "+str(exc)})

    if (nstatus == MemberStatus.PRIVATE):
        return HttpResponseRedirect(reverse("memberprofile"))
    elif (nstatus == MemberStatus.ARCHIVED):
            return render(request, "members/mylogin.html", {"message":"Your account is archived, please contact us for activating it!"})
    return HttpResponseRedirect(reverse("memberboard"))


def mylogout(request):
    if request.method != "GET":
       return HttpResponseNotAllowed(["GET"])
    if (request.user.is_authenticated == False):
        return HttpResponseRedirect(reverse("mylogin"))
    try:
        logout(request)
        return render(request, "members/mylogin.html", {"message":""})
    except:
        return render(request, "members/mylogin.html", {"message":"The logout has failed!"})


def mysignup(request):
    if (request.method == "GET"):
        return render(request, "members/mysignup.html", {"message":""})
    if (request.method != "POST"):
        return HttpResponseNotAllowed(["GET", "POST"])
    
    user = request.POST["username"]
    email = request.POST["email"]
    pwd = request.POST["password"]
    pdu = request.POST["passdupe"]
    if (len(user)>240 or len(email)>240 or len(pwd)>240 or len(pdu)>240):
        return HttpResponseBadRequest("Incorrect value(s)!")

    tx = ""
    if (len(user)<6 or len(pwd)<6 or len(pdu)<6 or len(email) < 6):
        tx = tx + "All input fields need to have at least 6 characters; "
    if (len(user)>50 or len(pwd)>50 or len(pdu)>50 or len(email)>50):
        tx = tx + "All input fields are limited to maximum 50 characters; "
    if (pwd != pdu):
        tx = tx + "The passwords are different!"
    if len(tx) > 0:
        return render(request, "members/mysignup.html", {"message":tx})

    try:
        buddy = User.objects.create_user(username = user, email = email, password = pwd)
        mybuddy = Member(djuser = buddy.username, 
                        djemail = buddy.email, 
                        name = buddy.username, 
                        stamp = getStamp())
        mybuddy.save()
        return render(request, "members/mylogin.html", {"message":""})
    except IntegrityError:
        return render(request, "members/mysignup.html", {"message":"The signup has failed because of duplicate user name or other database integrity problem!"})
    except Exception as exc:
        return render(request, "members/mysignup.html", {"message":"The signup has failed: "+str(exc)})            


def memberprofile(request):
    if (request.method == "GET"):
        buddy = getMember(request.user.username)
        if buddy is None or buddy.status == MemberStatus.ARCHIVED:                
            logout(request)
            return HttpResponseForbidden("Access not allowed!")    
        pubs = None
        withlist = False
        if buddy.status == MemberStatus.PUBLIC:           
            pubs = Network.objects.filter(status=NetworkStatus.PUBLIC).order_by("url")
            withlist = True
        ct = {"message":"", "name":buddy.name, "location":buddy.location, "social":buddy.social, "about":buddy.about, "withlist":withlist, "pubsocs":pubs}
        return render(request, "members/memberprofile.html", ct)

    if (request.method != "POST"):
        return HttpResponseNotAllowed(["GET", "POST"])
    
    buddy = getMember(request.user.username)
    if buddy is None or buddy.status == MemberStatus.ARCHIVED:               
        logout(request)
        return HttpResponseForbidden("Access not allowed!")

    ntx = 0
    name = request.POST["name"]
    if len(name) < 1 or len(name) > 80:
        ntx += 1
    location = request.POST["location"]
    if len(location) < 1 or len(location) > 80:
        ntx += 1
    social = request.POST["social"]
    if (len(social) > 160):
        ntx += 1
    about = request.POST["about"]
    if (len(about) > 240):
        ntx += 1
    if ntx > 0:
        return HttpResponseBadRequest("Incorrect data (missing name, missing location or other issue!")
    
    tx = ""
    social = social.lower()
    if len(name) < 2:
        tx = tx + "Name too short; "
    if len(location) < 2:
        tx = tx + "Location too short; "
    if len(social) > 0:
        rc = carveUrl(social)
        social = rc[0]
        tx = tx + rc[1]
        if len(rc[1]) < 1:
            rs = spotUrl(social, False)
            if rs is None:
                tx = tx + "social network not yet on file, please propose it; "
            else:
                if rs.status != NetworkStatus.PUBLIC:           
                    tx = tx + "website is in review or archived; "
            social = "https://" + social   
    # members with PRIVATE status don't get social network section
    pubs = None
    withlist = False
    if buddy.status == MemberStatus.PUBLIC:           
        pubs = Network.objects.filter(status=NetworkStatus.PUBLIC).order_by("url")
        withlist = True

    if (len(tx) > 0):        
        return render(request, "members/memberprofile.html", 
            {"message": tx, "name":name, "location":location, "social":social, "about":about, "withlist":withlist, "pubsocs":pubs})

    if buddy.status == MemberStatus.PRIVATE:
        buddy.status = MemberStatus.PUBLIC
    buddy.name = name
    buddy.location = location
    buddy.social = social
    buddy.about = about
    try:
        buddy.save()
    except Exception as exc:
        return render(request, "members/memberprofile.html", 
            {"message": str(exc), "name":name, "location":location, "social":social, "about":about, "withlist":withlist, "pubsocs":pubs})
    return HttpResponseRedirect(reverse("memberboard"))
      

def cancel_memberprofile(request):
    nstatus = getMemberStatus(request.user.username)
    if (nstatus is None or nstatus != MemberStatus.PUBLIC):
        logout(request)
        return HttpResponseRedirect(reverse("mylogin"))
    return HttpResponseRedirect(reverse("memberboard"))


def membernewtheme(request):
    if (request.method != "POST"):
        return HttpResponseNotAllowed(["POST"])
    
    name = request.POST["name"]
    if len(name) > 80:
        return HttpResponseBadRequest("Parameter too long!")
    buddy = getMember(request.user.username)
    if buddy is None or buddy.status != MemberStatus.PUBLIC:
        return HttpResponseForbidden("Access not allowed!")             

    tx = ""
    name = name.capitalize()
    if len(name) < 2:
        tx = tx + "Name too short; "
    theme = getTheme(name = name)
    if theme is not None and theme.status != ThemeStatus.ARCHIVED:
        tx = tx + "Theme name is duplicate; "
    if len(tx) > 0:
        return JsonResponse({"error":"yes", "message":tx})
    # insert
    try:
        theme = Theme(name = name, stamp = getStamp())
        theme.save()
    except Exception as exc:
        return JsonResponse({"error":"yes", "message":str(exc)})               
    return JsonResponse({"error":"no", "message":"ok"})


def membernewplatform(request):
    if (request.method != "POST"):
        return HttpResponseNotAllowed(["POST"])
    
    name = request.POST["name"]
    type = request.POST["type"]
    if len(name) > 80 or len(type) > 20 or type not in ["social", "resource"]:
        return HttpResponseBadRequest("Incorrect parameter(s)!")
    buddy = getMember(request.user.username)
    if buddy is None or buddy.status != MemberStatus.PUBLIC:
        return HttpResponseForbidden("Access not allowed!")            

    isPlatform = False if type == "social" else True;
    tx = ""
    name = name.lower()
    if len(name) < 11:
        tx = tx + "The URL is too short; "
    rs = carveUrl(name)
    name = rs[0]
    tx = tx + rs[1] 
    plat = getPlatform(url = name) if isPlatform else getNetwork(url = name)
    plat_archived = PlatformStatus.ARCHIVED if isPlatform else NetworkStatus.ARCHIVED
    if plat is not None and plat.status != plat_archived:
        tx = tx + "The URL is duplicate; "
    if (len(tx) > 0):
        return JsonResponse({"error":"yes", "message":tx})
    # insert
    try:
        if isPlatform:
            plat = Platform(url = name, stamp = getStamp())
        else:
            plat = Network(url = name, stamp = getStamp())
        plat.save()
    except Exception as exc:
        return JsonResponse({"error":"yes", "message":str(exc)})               
    return JsonResponse({"error":"no", "message":"ok"})


def themedetails(request, cid):
    if (request.method != "GET"):
        return HttpResponseNotAllowed(["GET"])
    if len(cid) > 18:
        return HttpResponseBadRequest("Parameter too long!")
    
    buddy = getMember(request.user.username)
    if buddy is None or buddy.status != MemberStatus.PUBLIC:
        return HttpResponseForbidden("Access not allowed!")    

    theme = getiTheme(cid)
    if theme is None:
        return HttpResponseNotFound("Theme not found!")
    if theme.status != ThemeStatus.PUBLIC:
        return HttpResponseForbidden("Theme not accessible!")
    sugs = theme.theme_suggestions.filter(status=SuggestionStatus.PUBLIC).order_by("-id")
    return render(request, "members/themedetails.html", {"name":theme.name, "tid":str(theme.id), "mid":buddy.id, "sugs":sugs})


def platformdetails(request, cid):
    if (request.method != "GET"):
        return HttpResponseNotAllowed(["GET"])
    if len(cid) > 18:
        return HttpResponseBadRequest("Parameter too long!")
    
    buddy = getMember(request.user.username)
    if buddy is None or buddy.status != MemberStatus.PUBLIC:
        return HttpResponseForbidden("Access not allowed!")    

    plt = getiPlatform(cid)
    if plt is None:
        return HttpResponseNotFound("Platform not found!")
    if plt.status != PlatformStatus.PUBLIC:
        return HttpResponseForbidden("Platform not accessible!")
    sugs = plt.platform_suggestions.filter(status=SuggestionStatus.PUBLIC).order_by("-id")
    return render(request, "members/platformdetails.html", {"url":plt.url, "pid":str(plt.id), "mid":buddy.id, "sugs":sugs})


def suggestionrecord(request):
    if (request.method != "POST"):
        return HttpResponseNotAllowed(["POST"])

    tid = request.POST["tid"]
    sid = request.POST["sid"]
    title = request.POST["title"]
    author = request.POST["author"]
    year = request.POST["year"]
    url = request.POST["url"]
    text = request.POST["text"]
    ntx = 0
    if (len(tid) < 1 or len(tid) > 18):
        ntx += 1
    if (len(sid) < 1 or len(sid) > 18):
        ntx += 1
    if (len(title) < 1 or len(title) > 80):
        ntx += 1
    if (len(url) < 11 or len(url) > 240):
        ntx += 1
    if (len(author)>160 or len(year)>4 or len(text)>240):
        ntx += 1
    if ntx > 0:
        return HttpResponseBadRequest("Parameter too short or too long!")

    url = url.lower()
    
    buddy = getMember(request.user.username)
    if buddy is None or buddy.status != MemberStatus.PUBLIC:
        return HttpResponseForbidden("Access not allowed!")    
                     
    tx = ""

    if sid != "0":
        osug = getiSuggestion(sid)
        if osug is None or osug.status != SuggestionStatus.PUBLIC:
            tx = tx + "Study material not accessible; "
        else:
            if osug.sender.id != buddy.id:
                return HttpResponseForbidden("Access not allowed!")

    if checkYearPublished(year) == False:
        tx = tx + "Incorrect Year; "

    otheme = getiTheme(tid)
    if otheme is None or otheme.status != ThemeStatus.PUBLIC:
        tx = tx + "theme not accessible; "

    crv = carveUrl(url)
    myurl = "https://" + crv[0]
    if len(crv[1]) < 1:
        odomain = spotUrl(crv[0], True)
        if odomain is None:
            tx = tx + "platform not yet on file, please propose it; "
        else:
            if odomain.status != PlatformStatus.PUBLIC:           
                tx = tx + "website is in review or archived; "       
    else:
        tx = tx + crv[1]

    odupli = Suggestion.objects.filter(url = myurl, status = SuggestionStatus.PUBLIC)
    if sid == "0":
        if len(odupli) > 0:
            tx = tx + "The URL is already on file; "
    else:
        if len(odupli) > 0:
            ocounter = 0
            for odup in odupli:
                if str(odup.id) != sid:
                    ocounter += 1
            if ocounter > 0:
                tx = tx + "The URL is listed on a different suggestion; "

    if len(tx) > 0:
        return JsonResponse({"error":"yes", "message":tx})

    try:
        if sid == "0":
            osug = Suggestion(text = text, 
                            url = myurl,
                            stamp = getStamp(),
                            sender = buddy,
                            subject = otheme,
                            author = author,
                            title = title,
                            published = year,
                            domain = odomain)
        else:
            osug.text = text
            osug.url = myurl
            osug.author = author
            osug.title = title
            osug.published = year
            osug.domain = odomain
        osug.save()
    except Exception as exc:
        return JsonResponse({"error":"yes", "message":str(exc)})
    return JsonResponse({"error":"no", "message":"ok", "old":sid, "new":str(osug.id)})


def itemdelete(request):
    if (request.method != "POST"):
        return HttpResponseNotAllowed(["POST"])
    cid = request.POST["cid"]
    ctype = request.POST["ctype"]
    if (len(cid) < 1 or len(cid) > 18 or len(ctype) < 1 or len(ctype) > 12):
        return HttpResponseBadRequest("Parameter too short or too long!")
    if ctype not in ["suggestion", "comment", "message"]:
        return HttpResponseBadRequest("Bad parameter value!")
    
    buddy = getMember(request.user.username)
    if buddy is None or buddy.status != MemberStatus.PUBLIC:
        return HttpResponseForbidden("Access not allowed!")    

    if ctype == "suggestion":
        osug = getiSuggestion(cid)
        if osug is None or osug.status != SuggestionStatus.PUBLIC:
            return JsonResponse({"error":"yes", "message":"Study material not accessible!"})
        else:
            if osug.sender.id != buddy.id:
                return HttpResponseForbidden("Access not allowed!")
        try:
            #osug.delete()
            osug.status = SuggestionStatus.HIDDEN
            osug.save()
        except IntegrityError:
            return JsonResponse({"error":"yes", "message":"There is not possible to hide a suggestion with comment(s)!"})
        except Exception as exc:
            return JsonResponse({"error":"yes", "message":str(exc)})
    elif ctype == "comment":
        ocom = getiComment(cid)
        if ocom is None or ocom.status != CommentStatus.PUBLIC:
            return JsonResponse({"error":"yes", "message":"Comment not accessible!"})
        else:
            if ocom.sender.id != buddy.id:
                return HttpResponseForbidden("Access not allowed!")
        try:
            #ocom.delete()
            ocom.status = CommentStatus.HIDDEN
            ocom.save()
        except Exception as exc:
            return JsonResponse({"error":"yes", "message":str(exc)})
    elif ctype == "message":
        omes = getiMessage(cid)
        if omes is None or omes.status != MessageStatus.PRIVATE:
            return JsonResponse({"error":"yes", "message":"Message not accessible!"})
        else:
            if omes.sender.id != buddy.id:
                return HttpResponseForbidden("Access not allowed!")
        try:
            #omes.delete()
            omes.status = MessageStatus.HIDDEN
            omes.save()
        except Exception as exc:
            return JsonResponse({"error":"yes", "message":str(exc)})

    return JsonResponse({"error":"no", "message":"ok"})


def commentlist(request, ctype, oid, cid):
    if (request.method != "GET"):
        return HttpResponseNotAllowed(["GET"])
    if len(oid) > 18 or len(cid) > 18 or len(ctype) > 1 or ctype not in ["t", "p", "m"]:
        return HttpResponseBadRequest("Incorrect parameter!")
    
    buddy = getMember(request.user.username)
    if buddy is None or buddy.status != MemberStatus.PUBLIC:
        return HttpResponseForbidden("Access not allowed!")    

    sugg = getiSuggestion(cid)
    if sugg is None:
        return HttpResponseNotFound("Suggestion not found!")
    if sugg.status != SuggestionStatus.PUBLIC:
        return HttpResponseGone("Suggestion not accessible!")
    cmnts = sugg.suggestion_comments.filter(status=CommentStatus.PUBLIC).order_by("-id")

    return render(request, "members/commentlist.html", {"title":sugg.title, "theme":sugg.subject.name, "sid":str(sugg.id), "mid":buddy.id, "cmnts":cmnts, "ctype":ctype, "oid":oid})


def commentrecord(request):
    if (request.method != "POST"):
        return HttpResponseNotAllowed(["POST"])
    sid = request.POST["sid"]
    cid = request.POST["cid"]
    text = request.POST["text"]

    ntx = 0
    if (len(cid) < 1 or len(cid) > 18):
        ntx += 1
    if (len(sid) < 1 or len(sid) > 18):
        ntx += 1
    if (len(text) < 10 or len(text) > 240):
        ntx += 1
    if ntx > 0:
        return HttpResponseBadRequest("Parameter too short or too long!")
    
    buddy = getMember(request.user.username)
    if buddy is None or buddy.status != MemberStatus.PUBLIC:
        return HttpResponseForbidden("Access not allowed!")    
                     
    tx = ""
    osug = getiSuggestion(sid)
    if osug is None or osug.status != SuggestionStatus.PUBLIC:
        tx = tx + "Study material not accessible; "

    if cid != "0":
        ocom = getiComment(cid)
        if ocom is None or ocom.status != CommentStatus.PUBLIC:
            tx = tx + "Comment not accessible; "
        else:
            if ocom.sender.id != buddy.id:
                return HttpResponseForbidden("Access not allowed!")

    if len(tx) > 0:
        return JsonResponse({"error":"yes", "message":tx})            

    try:
        if cid == "0":
            ocom = Comment(text = text, 
                            stamp = getStamp(),
                            sender = buddy,
                            proposal = osug)
        else:
            ocom.text = text
        ocom.save()
    except Exception as exc:
        return JsonResponse({"error":"yes", "message":str(exc)})
    return JsonResponse({"error":"no", "message":"ok", "old":cid, "new":str(ocom.id)})


def itemflag(request):
    if (request.method != "POST"):
        return HttpResponseNotAllowed(["POST"])
    ctype = request.POST["ctype"]
    cid = request.POST["cid"]
    text = request.POST["text"]
    if (len(cid) < 1 or len(cid) > 18 or len(ctype) < 1 or len(ctype) > 20 or len(text) < 20 or len(text) > 240):
        return HttpResponseBadRequest("Parameter too short or too long!")
    if ctype not in ["suggestion", "comment", "message", "profile"]:
        return HttpResponseBadRequest("Bad parameter value!")

    buddy = getMember(request.user.username)
    if buddy is None or buddy.status != MemberStatus.PUBLIC:
        return HttpResponseForbidden("Access not allowed!")    
                     
    if ctype == "comment":
        ocom = getiComment(cid)
        if ocom is None or ocom.status != CommentStatus.PUBLIC:
            return JsonResponse({"error":"yes", "message":"Comment not accessible!"})
        else:
            if ocom.sender.id == buddy.id:
                return HttpResponseForbidden("Operation not allowed!")
        try:
            oflag = Flag( text = text,
                        itemid = ocom.id,
                        itemtype = ItemType.COMMENT,
                        stamp = getStamp(),
                        sender = buddy)
            oflag.save()
        except Exception as exc:
            return JsonResponse({"error":"yes", "message":str(exc)})                    
    elif ctype == "suggestion":
        osug = getiSuggestion(cid)
        if osug is None or osug.status != SuggestionStatus.PUBLIC:
            return JsonResponse({"error":"yes", "message":"Study material not accessible!"})
        else:
            if osug.sender.id == buddy.id:
                return HttpResponseForbidden("Operation not allowed!")
        try:
            oflag = Flag( text = text,
                        itemid = osug.id,
                        itemtype = ItemType.SUGGESTION,
                        stamp = getStamp(),
                        sender = buddy)
            oflag.save()
        except Exception as exc:
            return JsonResponse({"error":"yes", "message":str(exc)})                
    elif ctype == "message":
        omes = getiMessage(cid)
        if omes is None or omes.status != MessageStatus.PRIVATE:
            return JsonResponse({"error":"yes", "message":"Message not accessible!"})
        else:
            if omes.sender.id == buddy.id:
                return HttpResponseForbidden("Operation not allowed!")
        try:
            oflag = Flag( text = text,
                        itemid = omes.id,
                        itemtype = ItemType.MESSAGE,
                        stamp = getStamp(),
                        sender = buddy)
            oflag.save()
        except Exception as exc:
            return JsonResponse({"error":"yes", "message":str(exc)})
    elif ctype == "profile":
        omem = getiMember(cid)
        if omem is None or omem.status != MemberStatus.PUBLIC:
            return JsonResponse({"error":"yes", "message":"Member profile is not accessible!"})
        else:
            if omem.id == buddy.id:
                return HttpResponseForbidden("Operation not allowed!")
        try:
            oflag = Flag( text = text,
                        itemid = omem.id,
                        itemtype = ItemType.PROFILE,
                        stamp = getStamp(),
                        sender = buddy)
            oflag.save()
        except Exception as exc:
            return JsonResponse({"error":"yes", "message":str(exc)})

    return JsonResponse({"error":"no", "message":"ok"})


def incominglist(request):
    if (request.method != "GET"):
        return HttpResponseNotAllowed(["GET"])
    
    buddy = getMember(request.user.username)
    if buddy is None or buddy.status != MemberStatus.PUBLIC:
        return HttpResponseForbidden("Access not allowed!") 

    incs = buddy.member_received.filter(status = MessageStatus.PRIVATE).order_by("-id")
    return render(request, "members/incominglist.html", {"incs":incs})


def outgoinglist(request):
    if (request.method != "GET"):
        return HttpResponseNotAllowed(["GET"])
    
    buddy = getMember(request.user.username)
    if buddy is None or buddy.status != MemberStatus.PUBLIC:
        return HttpResponseForbidden("Access not allowed!")    

    outs = buddy.member_sent.filter(status = MessageStatus.PRIVATE).order_by("-id")
    return render(request, "members/outgoinglist.html", {"outs":outs})


def memberdetails(request, cid):
    if (request.method != "GET"):
        return HttpResponseNotAllowed(["GET"])
    if len(cid) > 18:
        return HttpResponseBadRequest("Parameter too long!")
    
    mebuddy = getMember(request.user.username)
    if mebuddy is None or mebuddy.status != MemberStatus.PUBLIC:
        return HttpResponseForbidden("Access not allowed!")    
    
    gobuddy = getiMember(cid)
    if gobuddy is None or gobuddy.status != MemberStatus.PUBLIC:
        return HttpResponseForbidden("Access not allowed!")    

    golist = gobuddy.member_suggestions.filter(status = SuggestionStatus.PUBLIC).order_by("-id")
    return render(request, "members/memberdetails.html", {"meid":str(mebuddy.id), "goid":str(gobuddy.id), "gobuddy":gobuddy, "golist":golist})


def privatemessage(request):
    if (request.method != "POST"):
        return HttpResponseNotAllowed(["POST"])
    toid = request.POST["toid"]
    ctext = request.POST["ctext"]
    if (len(toid) < 1 or len(toid) > 18 or len(ctext) < 10 or len(ctext) > 240):
        return HttpResponseBadRequest("Parameter too short or too long!")
    
    frombuddy = getMember(request.user.username)
    if frombuddy is None or frombuddy.status != MemberStatus.PUBLIC:
        return HttpResponseForbidden("Access not allowed!")    
    
    tobuddy = getiMember(toid)
    if tobuddy is None or tobuddy.status != MemberStatus.PUBLIC:
        return HttpResponseForbidden("Access not allowed!")    

    try:
        oprime = Message( text = ctext,
                    stamp = getStamp(),
                    recipient = tobuddy,
                    sender = frombuddy)
        oprime.save()
    except Exception as exc:
        return JsonResponse({"error":"yes", "message":str(exc)})

    return JsonResponse({"error":"no", "message":"ok"})
    