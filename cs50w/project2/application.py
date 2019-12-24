import os, json, datetime
from collections import deque
from urllib.parse import unquote

################### constants for validating input data
user_limit = 30 # maximum user name length
channel_limit = 50 # maximum channel name length
message_limit = 250 # maximum message length

###################
# building a dummy database, employing GLOBAL variables (as required)
# - the "buddies" dictionary contains the user names
# - the "channels" dictionary contains dynamically changing data
#   - dictionary keys are channel names
#   - dictionary values are deques of message items
#   - private messages are added into a channel name starting with "~" and followed by the user name
# This is a POC! Don't use shared & writable memory variables for multithreaded solutions!
###################

# as required - the latest 100 messages are stored in server memory
deque_limit = 100
# server-side disk storage used upon application start, and the "Save" button (on the admin's UI)
myfile = "mess.json"
# for workup (deques cannot be handled by the json module)
myerrorlog = "socketerrors.log"
mess = dict() 
# server-side memory storage
channels = dict()

buddies = {"adam white":".", "cindy long":".", "mary smith":".", "tim johns":".", "sally atkins":".", "jane doe":".", "admin":"+"}

# save "database"
def my_write_globs():
    for key in channels:
        mess[key] = list(channels[key])
    with open(myfile, "w") as fh:
        json.dump(mess, fh)
    mess.clear()

# log error
def mylog(cText):
    with open(myerrorlog, "a+") as fh:
        fh.write(cText + "\n")
        fh.write(datetime.datetime.now().strftime("%x %X") + "\n")


# backup "database"
if (os.path.exists(myfile)):
    with open(myfile, "r") as fh:
        mess = json.load(fh)
    for key in mess:
        channels[key] = deque(mess[key], maxlen = deque_limit)
    mess.clear()


################### start flask

from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_socketio import SocketIO, emit, join_room, leave_room

app = Flask(__name__)
app.config["SECRET_KEY"] = "exercise"
socketio = SocketIO(app)

################### endpoints

@app.route("/", methods=["GET", "POST"])
def home():
    return render_template("home.html")


@app.route("/chat/<buddy>", methods=["GET", "POST"])
def chat(buddy):
    username = unquote(buddy)
    if username not in buddies:
        return "User not found!", 404
    special = True if buddies[username] == "+" else False
    return render_template("chat.html", admin = special)


@app.route("/saveall", methods=["GET"])
def saveall():
    my_write_globs()
    return ("Dummy data is saved now!")


@app.route("/checkuser", methods=["POST"])
def checkuser():
    name = request.form.get("name")
    name = name.strip() if name is not None else ""
    if len(name)<2 or len(name)>user_limit:
        return ("User name too short or too long!"), 422
    if name in buddies:
        return ("done")
    else:
        return ("User not found!"), 404


@app.route("/createchannel", methods=["POST"])
def createchannel():
    name = request.form.get("name")
    name = name.strip() if name is not None else ""
    if len(name)<2 or len(name)>channel_limit:
        return ("Channel name too short or too long!"), 422       
    if name in channels:
        return ("The channel already exists!"), 403
    channels[name] = deque(maxlen = deque_limit)
    # broadcasting the new channel name
    socketio.emit("server_new_channel", {"name":name})
    return ("done")


@app.route("/listchannel", methods=["POST"])
def listchannel():
    name = request.form.get("name")
    name = name.strip() if name is not None else ""
    if len(name)<2 or len(name)>channel_limit:
        return ("Channel name too short or too long!"), 422       
    chan = channels.get(name)
    if chan is None:
        if (name[:1] == "~"):
            return ("So far you haven't received any message!"), 404
        else:
            return ("Channel not found!"), 404

    dummy = dict();
    counter = 0
    for elem in chan:
        counter = counter + 1
        dummy[str(counter)] = {"user":elem[0], "text":elem[1], "stamp":elem[2]};
    return jsonify(dummy)


@app.route("/listchannels", methods=["POST"])
def listchannels():
    if len(channels) < 1:
        return ("Channels not found!"), 404
    else:
        mylist = list(channels.keys())
        dummy = dict()
        counter = 0
        for elem in mylist:
            if (elem[:1] == "~"):
                continue
            counter = counter + 1
            dummy[str(counter)] = elem
        return jsonify(dummy)

#################################### websocket events

@socketio.on("client_new_message")
def new_message(data):
    # logging malformed input
    m1 = data["user"]
    if m1 not in buddies:
        mylog("Sender not found: " + m1)
        return
    m2 = data["channel"]
    if (m2[:1] == "~" and m2[1:] not in buddies):
        mylog("Recipient not found: " + m2)
        return
    if (m2[:1] != "~" and m2 not in channels):
        mylog("Channel not found: " + m2)
        return
    m3 = data["text"]
    if m3 is None or len(m3) < 2 or len(m3) > message_limit:
        mylog("User: " + m1 + " Channel: " + m2 + " Incorrect message text: " + m3)
        return
    # the new users initially don't have a private channel
    if (m2[:1] == "~" and m2 not in channels):
        channels[m2] = deque(maxlen = deque_limit)
    # adding time stamp
    m4 = datetime.datetime.now().strftime("%x %X")
    channels[m2].append([m1, m3, m4])
    # broadcasting for online users in the room
    if (m2[:1] != "~"):
        emit("server_new_message", {"user":m1, "channel":m2, "text":m3, "stamp":m4}, room = m2)


@socketio.on("join_channel")
def client_join_room(data):
    clientChannel = data["room"]
    if (clientChannel is None or len(clientChannel)<2 or len(clientChannel)>channel_limit):
        mylog("Incorrect channel name (when joining): "+clientChannel)
        emit("test", "422", "Incorrect channel name!")
        return
    if clientChannel not in channels:
        mylog("Channel not found (when joining): "+clientChannel)
        emit("test", "404", "Channel not found!")
        return
    join_room(clientChannel)
    #mylog("Joined: " + clientChannel)


@socketio.on("leave_channel")
def client_leave_room(data):
    clientChannel = data["room"]
    if (clientChannel is None or len(clientChannel)<2 or len(clientChannel)>channel_limit):
        mylog("Incorrect channel name (when leaving): " + clientChannel)
        emit("test", "422", "Incorrect channel name!")
        return
    leave_room(clientChannel)
    #mylog("Left: " + clientChannel)


@socketio.on_error()
def socket_error_handler(exc):
    mylog(str(exc))


################## Comment written in December 2019
# The below launching solution is needed 
# for pacifying python 3.8 and flask_socketio and debug mode.
# Additionally you need to start flask with the command
# "python application.py" instead of the command "flask run"
# in order to get it right (socketio does start only on the main thread)
##################

if __name__ == '__main__':
    socketio.run(app)
