/////////////////////////////////////// initializing window-level variables

    let currentUser = "";
    let currentChannel = "";
    let mysocket = null;

mysocket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

////////////////////////////////////////// helper functions for DOM updates

function initList(qParent, qOld) {
    const nodeParent = document.querySelector('.'+qParent);
    if (!nodeParent) return false;
    const nodeOld = document.querySelector('.'+qOld);
    if (nodeOld) {
        let obj = nodeParent.removeChild(nodeOld);
        obj = null;
    }
    const nodeNew = document.createElement("div");
    nodeNew.className = qOld;
    const spec = document.createElement("div");
    spec.className = qOld + "-coda";
    nodeNew.appendChild(spec);
    nodeParent.appendChild(nodeNew);
    return nodeNew;
}

function insertMessage(oParent, cUser, cStamp, cText) {
    const newDiv = document.createElement("div");
    //newDiv.className = "eis-mess-entry";
    const newPar1 = document.createElement("p");
    newPar1.className = "eis-text-wrap";

    const span1 = document.createElement("span");
    span1.className = "eis-entry";
    span1.textContent = cUser;
    span1.onclick = function() {
        if (this.textContent == currentUser) {
            alert("You cannot send message to yourself!");
            return false;
        }
        const obj = document.querySelector("#private_title");
        if (obj) obj.textContent = this.textContent;
        document.querySelector("#name_private_chat").value = "";
        document.querySelector("#show_private_chat").style.display = "block";
        return false;
    };

    const span2 = document.createElement("span");
    span2.textContent = " " + cStamp;
    newPar1.appendChild(span1);
    newPar1.appendChild(span2);
    const newPar2 = document.createElement("p");
    newPar2.textContent = cText;
    newDiv.appendChild(newPar1);
    newDiv.appendChild(newPar2);
    oParent.insertBefore(newDiv, oParent.firstChild);
}

function insertChannel(oParent, title) {
    const n1 = document.createElement("div");
    n1.className = "eis-text-wrap";
    const n2 = document.createElement("span");
    n2.className = "eis-entry";
    //n2.href = "";
    n2.textContent = title;
    n2.onclick = function() {
        if (currentChannel.length > 1) {
            mysocket.emit("leave_channel",  {"room":currentChannel});
        }
        currentChannel = this.textContent;
        pullChannelPosts(true);
        return false;
    }; 
    n1.appendChild(n2);
    oParent.insertBefore(n1, oParent.firstChild);
}

//////////////////////////////////////////// getting latest posts

function pullChannelPosts(isPublic) {
    document.querySelector("#eis_mess").style.display = "block";
    const tit = document.querySelector("#eis-mess-channel");
    const ico = document.querySelector("#menu_chat");
    if (tit) {
        if (isPublic === false) {
            if (ico) ico.style.display = "none";
            tit.textContent = "Your Private Messages";
        } else {
            if (ico) ico.style.display = "inline-block";
            tit.textContent = currentChannel;
        }
    }
    
    const obj = initList("eis-mess-body", "eis-mess-list");

    const xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
        try {
            if (this.readyState == 4) {
                if (this.status == 404 || this.status == 422) throw new Error(this.responseText);
                if (this.status < 200 || this.status > 299) throw new Error(this.statusText);
                const resp = JSON.parse(this.responseText);
                const obj = document.querySelector(".eis-mess-list");
                if (!obj) throw new Error("Error while initializing message list!");								
                for (elem in resp) {
                    insertMessage(obj,resp[elem]["user"], resp[elem]["stamp"], resp[elem]["text"] );
                }
                //document.querySelector("#eis_mess").style.display = "block";
                if (currentChannel.substring(0,1) !== "~") {
                    mysocket.emit("join_channel", {"room":currentChannel});
                }
            }
        } catch (err) {
            alert(err.message);
        }
    }

    try {
        xhr.open("POST", "/listchannel", true);
        xhr.timeout = 60000;
        const data = new FormData();
        data.append("name", currentChannel);
        xhr.send(data);						
    }
    catch (err) {
        alert(err.message)
    }
}

/////////////////////////////////////////// getting the latest channel list

function pullTitles() {			
    const xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
        try {
            if (this.readyState == 4) {
                if (this.status == 404) {
                    const obj = initList("eis-chan-body", "eis-chan-list");
                    if (!obj) throw new Error("Error while creating channel list!");
                }
                else if (this.status < 200 || this.status > 299) {
                    throw new Error(this.statusText);
                }
                const res = JSON.parse(this.responseText);
                const obj = initList("eis-chan-body", "eis-chan-list");
                if (!obj) throw new Error("Error while creating channel list!");
                // adding channel titles
                for (const pos in res) {
                    insertChannel(obj, res[pos].toString());
                }
            }
        } catch (err) {
            alert(err.message);
        }
    };

    try {
        xhr.open("POST", "/listchannels", true);
        xhr.timeout = 30000;
        xhr.send();						
    }
    catch (err) {
        alert(err.message)
    }									
}
        
//////////////////////////////////////////////////// upon page load add listeners to certain elements

document.addEventListener('DOMContentLoaded', function() {
    // pick up current user and channel (saved locally)
    currentUser = localStorage.getItem('currentUser');	
    currentChannel = localStorage.getItem('currentChannel');
    
    // hit button "add new channel"
    document.querySelector("#menu_add").onclick = function() {
        document.querySelector("#name_new_channel").value = "";
        document.querySelector("#show_new_channel").style.display = "block";
        return false;
    };
    
    // hit button "hide channel"
    document.querySelector("#chan_roll").onclick = function() {
        const obj = document.querySelector("#eis_chan");
        if (obj) obj.style.display = "none";
        return false;
    };

    // hit "cancel message" in public channel
    document.querySelector("#cancel_chat").onclick = function() {
        document.querySelector("#show_chat").style.display = "none";
        return false;
    };

    // hit "cancel message" in private message list
    document.querySelector("#cancel_private_chat").onclick = function() {
        document.querySelector("#show_private_chat").style.display = "none";
        return false;
    };

    // hit button for starting new chat
    document.querySelector("#menu_chat").onclick = function() {
        document.querySelector("#name_chat").value = "";
        const obj = document.querySelector("#show_chat").style.display = "block";
        return false;
    }

    // hit button for displaying channel list
    document.querySelector("#menu_list").onclick = function() {
        const obj = document.querySelector("#eis_chan");
        if (obj) obj.style.display = "block";
        return false;
    };

    // hit "cancel" instead of adding new channel name
    document.querySelector("#cancel_new_channel").onclick = function() {
        document.querySelector("#show_new_channel").style.display = "none";
        return false;
    };


    // hit "submit" new channel name
    document.querySelector("#send_new_channel").onclick = function() {
        let name = document.querySelector("#name_new_channel").value;
        if (name == null) return false;
        name = name.trim();						
        if (name.length < 2 || name.length > 50) {
            alert("The channel name needs to have between 2 and 50 characters!");
            return false;
        }
        if (name.substring(0,1) === "~") {
            alert("The channel name cannot start with '~' (tilde) symbol!");
            return false;
        }

        const xhr = new XMLHttpRequest();
        xhr.onreadystatechange = function() {
            try {
                if (this.readyState == 4) {
                    if (this.status == 403 || this.status == 422) throw new Error(this.responseText);
                    if (this.status < 200 || this.status > 299) throw new Error(this.statusText);
                    document.querySelector("#show_new_channel").style.display = "none";
                }
            } catch (err) {
                alert(err.message);
            }
            return false;
        }

        try {
            xhr.open("POST", "/createchannel", true);
            xhr.timeout = 30000;
            const data = new FormData();
            data.append("name", name);
            xhr.send(data);						
        }
        catch (err) {
            alert(err.message);
        }

        return false;
    };

    // for development only: on the server it saves (into a file on the disk) the currently available text content
    const icon_menu_save = document.querySelector("#menu_save");
    if (icon_menu_save) icon_menu_save.onclick = function() {
        specialStuff();
        return false;
    };

    // hit icon for displaying private message list
    document.querySelector("#menu_private").onclick = function() {
        if (currentChannel.length > 1) {
            mysocket.emit("leave_channel",  {"room":currentChannel});
        }
        currentChannel = "~" + currentUser;
        pullChannelPosts(false);
        return false;					
    }

    //////////////////////////////////////////////// manage socket

    // hit "submit" public chat message
    document.querySelector("#send_chat").onclick = function() {
        let tx = document.querySelector("#name_chat").value;
        if (tx == null) return false;
        tx = tx.trim();						
        if (tx.length < 2 || tx.length > 250) {
            alert("The message needs to have between 2 and 250 characters!");
            return false;
        }

        try {
            mysocket.emit("client_new_message", {"user":currentUser, "channel":currentChannel, "text":tx});
            document.querySelector("#show_chat").style.display = "none";
        }
        catch (err) {
            alert(err.message);
        }

        return false;
    };


    // send private chat message
    document.querySelector("#send_private_chat").onclick = function() {
        let tx = document.querySelector("#name_private_chat").value;
        if (tx == null) return false;
        tx = tx.trim();						
        if (tx.length < 2 || tx.length > 250) {
            alert("The message needs to have between 2 and 250 characters!");
            return false;
        }

        try {
            let target = document.querySelector("#private_title").textContent;
            target = "~" + target;
            mysocket.emit("client_new_message", {"user":currentUser, "channel":target, "text":tx});
            document.querySelector("#show_private_chat").style.display = "none";
        }
        catch (err) {
            alert(err.message);
        }

        return false;
    };


    // receive new channel
    mysocket.on("server_new_channel", function(resp) {
        const obj = document.querySelector(".eis-chan-list");
        try {
            if (!obj) throw new Error("Missing list parent element!");
            insertChannel(obj, resp.name.toString());
        } catch (err) {
            console.log(err.message);
        }
    });


    // receive new message
    mysocket.on("server_new_message", function(resp) {
        if (resp.channel != currentChannel) return;
        const obj = document.querySelector(".eis-mess-list");
        try {
            if (!obj) throw new Error("Missing list parent element!");
            insertMessage(obj, resp.user, resp.stamp, resp.text);
        } catch (err) {
            console.log(err.message);
        }
    });

    //////////////////////////////////////////////// show stuff

    document.querySelector("#eis_menu").style.display = "block";
    document.querySelector("#eis_chan").style.display = "block";

    pullTitles();
    if (typeof currentChannel === "string" && currentChannel.length > 1) {
        if (currentChannel.substring(0, 1) === "~") {
            pullChannelPosts(false);
        } else {
            pullChannelPosts(true);
        }
    } else {
        document.querySelector("#eis_mess").style.display = "none";
    }

});

//////////////////////////////////////////////////////////// final to-do

window.addEventListener('beforeunload', function(event) {
    localStorage.setItem("currentChannel", currentChannel);
    mysocket.close();
});
