import json, datetime
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponseNotAllowed, JsonResponse
from .models import Group, Product, Offer, Part, Extra, OrderHeader, OrderDetail
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.urls import reverse
from django.db import IntegrityError

def home(request):
    if request.method != "GET":
        return
    if (request.user is None or request.user.is_authenticated == False):
        return HttpResponseRedirect(reverse("mylogin"))
    else:
        if (request.user.is_staff):
            return HttpResponseRedirect(reverse("staffboard"))
        else:
            return HttpResponseRedirect(reverse("clientboard"))


def clientorderlist(request):
    ckey = request.user.username
    # get order list in "latest first" order
    reslist = OrderHeader.objects.filter(client__exact=ckey).order_by("-stamp")
    # prepare a dictionary and send it back
    dres = {}
    dcounter = 0
    for elem in reslist:
        dcounter = dcounter+1
        cdate = elem.stamp[5:10] + elem.stamp[4:5] + elem.stamp[2:4]
        dres[str(dcounter)] = {"id":str(elem.id), 
                                "val":str(round(elem.total, 2)), 
                                "date":cdate,
                                "status":elem.status}
    return JsonResponse(dres)


def stafforderlist(request):
    # get all orders
    ords = OrderHeader.objects.all()
    dords = {}
    for elem in ords:
        cdate = elem.stamp[5:10] + elem.stamp[4:5] + elem.stamp[2:4] + " " + elem.stamp[11:16]
        delem = { "client":elem.client,
                "stamp":cdate, 
                 "total":str(round(elem.total, 2)), 
                 "status":elem.status}
        dlist = list()
        # get all order details for a specific order
        dets = elem.orderdetails.all()
        if dets is None or len(dets) < 1:
            continue
        for ele in dets:
            nm = ele.name
            if (len(ele.namex) > 0):
                nm = ele.name + ", " + ele.namex
            pr = str(round(ele.price + ele.pricex, 2))
            qt = str(round(ele.quantity, 2))
            dlist.append({"n":nm, "p":pr, "q":qt})
        delem["list"] = dlist
        dords[str(elem.id)] = delem
    return JsonResponse(dords)


def stafforderstatus(request):
    nid = request.POST["id"]
    cstatus = request.POST["status"]
    try:
        elem = OrderHeader.objects.filter(id__exact=nid).first()
        elem.status = cstatus
        elem.save()
        return JsonResponse({"error":"no"})
    except Exception as exc:
        return JsonResponse({"error":"yes", "message":str(exc)})


def neworder(request):
    try:
        cart = json.loads(request.POST["serialcart"])
        stamp = datetime.datetime.now()
        order_h = OrderHeader(client = request.user.username, 
            total = cart["0"]["total"], 
            status = "placed", 
            stamp = str(stamp))
        order_h.save()
        order_id = order_h.id

        for ckey in cart:
            if ckey == "0":
                continue
            order_d = OrderDetail(oid = order_h,
                name = cart[ckey]["name"],
                namex = cart[ckey]["namex"],
                price = cart[ckey]["price"],
                pricex = cart[ckey]["pricex"],
                quantity = cart[ckey]["quantity"],
                total = cart[ckey]["total"],
                gid = cart[ckey]["gid"],
                pid = cart[ckey]["pid"],
                tid = cart[ckey]["tid"] )
            order_d.save()

        return JsonResponse({"error":"no", "message":str(order_id)})
    except Exception as exc:
        return JsonResponse({"error":"yes", "message":str(exc)})
        

def mylogin(request):
    if (request.method == "GET"):
        return render(request, "orders/mylogin.html", {"message":""})
    if (request.method != "POST"):
        return

    user = request.POST["username"]
    user = "" if user is None else user.strip()
    pwd = request.POST["password"]
    pwd = "" if pwd is None else pwd.strip()

    if (len(user)<3 or len(pwd)<3):
        return render(request, "orders/mylogin.html", {"message":"User name and password need to have at least 3 characters!"})
    if (len(user)>50 or len(pwd)>50):
        return render(request, "orders/mylogin.html", {"message":"User name and password are limited to maximum 50 characters!"})

    try:
        resp = authenticate(request, username = user, password = pwd)
        if (resp):
            login(request, resp)           
        else:
            return render(request, "orders/mylogin.html", {"message":"The login has failed!"})
    except Exception as exc:
        return render(request, "orders/mylogin.html", {"message":"The authentication has failed: "+str(exc)})            

    if (request.user.is_staff):
        return HttpResponseRedirect(reverse("staffboard"))
    else:
        return HttpResponseRedirect(reverse("clientboard"))
    

def mylogout(request):
    if request.method != "GET":
       return
    if (request.user is None or request.user.is_authenticated == False):
        return HttpResponseRedirect(reverse("mylogin"))

    try:
        logout(request)
        return render(request, "orders/mylogin.html", {"message":""})
    except:
        return render(request, "orders/mylogin.html", {"message":"The logout has failed!"})


def mysignup(request):
    if (request.method == "GET"):
        return render(request, "orders/mysignup.html", {"message":""})
    if (request.method != "POST"):
        return

    user = request.POST["username"]
    user = "" if user is None else user.strip()
    pwd = request.POST["password"]
    pwd = "" if pwd is None else pwd.strip()
    pdu = request.POST["passdupe"]
    pdu = "" if pdu is None else pdu.strip()
    mail = request.POST["email"]
    mail = "" if mail is None else mail.strip()
    fnam = request.POST["first_name"]
    fnam = "" if fnam is None else fnam.strip()
    lnam = request.POST["last_name"]
    lnam = "" if lnam is None else lnam.strip()

    if (len(user)<3 or len(pwd)<3 or len(pdu)<3 or len(fnam)<3 or len(lnam)<3 or len(mail)<3):
        return render(request, "orders/mysignup.html", {"message":"All input fields need to have at least 3 characters!"})
    if (len(user)>50 or len(pwd)>50 or len(pdu)>50 or len(fnam)>50 or len(lnam)>50 or len(mail)>50):
        return render(request, "orders/mysignup.html", {"message":"All input fields are limited to maximum 50 characters!"})
    if (pwd != pdu):
        return render(request, "orders/mysignup.html", {"message":"The passwords are different!"})

    try:
        buddy = User.objects.create_user(user, mail, pwd)
        buddy.first_name = fnam
        buddy.last_name = lnam
        return render(request, "orders/mylogin.html", {"message":""})
    except IntegrityError:
        return render(request, "orders/mysignup.html", {"message":"The signup has failed because of duplicate user name or other database integrity problem!"})            
    except Exception as exc:
        return render(request, "orders/mysignup.html", {"message":"The signup has failed: "+str(exc)})            


#@ensure_csrf_cookie
def clientboard(request):
    dlist = list()
    for pr in Product.objects.all():
        for elem in pr.types.all():
            dlist.append({"gid":str(pr.category.id), "gname":pr.category.name, "pid":str(pr.id), "pname":pr.name, "tid":str(elem.id), "tname":elem.name, "price":elem.price, "parts":str(pr.parts), "extras":str(pr.extras)})
    return render(request, "orders/clientboard.html", {"dlist":dlist, "dpart":Part.objects.all(), "dextra":Extra.objects.all()})


#@ensure_csrf_cookie
def staffboard(request):
    dlist = list()
    for pr in Product.objects.all():
        for elem in pr.types.all():
            dlist.append({"category":pr.category, "name":pr.name, "type":elem.name, "price":elem.price})
    return render(request, "orders/staffboard.html", {"dlist":dlist})
