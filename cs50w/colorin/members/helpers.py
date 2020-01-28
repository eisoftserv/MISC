from datetime import datetime
from members.models import Member, Platform, Network, Theme, Suggestion, Comment, Message, Flag

def checkYearPublished(cval):
    if (len(cval) < 1):
        return True
    try:
        nval = int(cval)
    except:
        nval = -1
    if nval < 1000:
        return False
    if datetime.now().year < nval:
        return False
    return True  

def carveUrl(name):
    tx = ""
    if name.endswith("/") or name.endswith("\\"):
        name = name[:-1]
    if (name.startswith("https://www.") == True):
        name = name[12:]
    else:
        if (name.startswith("https://") == False):
            tx = "the URL must start with https:// ; "
        else:
            name = name[8:]
    pos = name.find(".")
    if pos < 0:
        tx = tx + "malformed domain name; "
    return [name, tx]

def spotUrl(name, isPlatform):
    ckey = name
    npos = name.find("/")
    if npos > 0:
        ckey = name[:npos]
    if isPlatform:
        obj = Platform.objects.filter(url__startswith=ckey).first()
    else:
        obj = Network.objects.filter(url__startswith=ckey).first()
    return obj

def getStamp():
    return (str(datetime.now())[:19])

def getMember(dj):
    try:
        buddy = Member.objects.get(djuser = dj)
    except:
        buddy = None
    return buddy

def getiMember(id):
    try:
        buddy = Member.objects.get(id = id)
    except:
        buddy = None
    return buddy

def getMemberStatus(dj):
    try:
        buddy = Member.objects.get(djuser = dj)
    except:
        buddy = None
    if buddy is None:
        return None
    return buddy.status

def getTheme(name):
    try:
        theme = Theme.objects.get(name__iexact = name)
    except:
        theme = None
    return theme

def getiTheme(id):
    try:
        theme = Theme.objects.get(id = id)
    except:
        theme = None
    return theme

def getThemeStatus(name):
    try:
        theme = Member.objects.get(name__iexact = name)
    except:
        theme = None
    if theme is None:
        return None
    return theme.status

def getPlatform(url):
    try:
        plt = Platform.objects.get(url = url)
    except:
        plt = None
    return plt

def getiPlatform(id):
    try:
        plt = Platform.objects.get(id = id)
    except:
        plt = None
    return plt

def getNetwork(url):
    try:
        netw = Network.objects.get(url = url)
    except:
        netw = None
    return netw

def getiNetwork(id):
    try:
        netw = Network.objects.get(id = id)
    except:
        netw = None
    return netw

def getPlatformStatus(url):
    try:
        plt = Member.objects.get(url = url)
    except:
        plt = None
    if plt is None:
        return None
    return plt.status

def getiSuggestion(id):
    try:
        sugg = Suggestion.objects.get(id = id)
    except:
        sugg = None
    return sugg

def getiComment(id):
    try:
        cmnt = Comment.objects.get(id = id)
    except:
        cmnt = None
    return cmnt

def getiMessage(id):
    try:
        cmnt = Message.objects.get(id = id)
    except:
        cmnt = None
    return cmnt

def getiFlag(id):
    try:
        ofl = Flag.objects.get(id = id)
    except:
        ofl = None
    return ofl
