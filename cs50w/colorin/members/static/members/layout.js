
///////////////////////////////////// shared JS code

function showCustomAlert(message, withTick) {    
    document.querySelector("#mess_message").textContent = message;
    if (withTick == true) document.querySelector("#mess_tick").style.display = "block";
    document.querySelector("#mess_wait").style.display = "block";
}

function hideCustomAlert() {    
    document.querySelector("#mess_tick").style.display = "none";
    document.querySelector("#mess_wait").style.display = "none";
}

function extractToken() {
    let token = "";
    const pairs = document.cookie.split(";");
    pairs.forEach( ele => { 
        if (ele.startsWith("csrftoken=")) token = ele.substring(10);
    });
    return token;
}

////////////////////////////////////////////////////
// custom application object "myclient" - compatible with IE11
////////////////////////////////////////////////////

const myclient = { "send":null, "failure":null, "success":null, minHeight:2000 };
myclient.failure = function(mess) {
    hideCustomAlert();
    showCustomAlert(mess, true);
    return false;
};
myclient.success = function(resp) {
    hideCustomAlert();
    showCustomAlert("The 'success' function is not yet implemented!", true);
    return false;
}
myclient.send = function( data_dict, op_type, url, time_limit) {
    const xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
        try {
            if (this.readyState == 4) {
                if (this.status < 200 || this.status > 299) myclient.failure(this.statusText);
                try {
                    const resp = JSON.parse(this.responseText);                    
                    if (typeof(resp) !== "object" || Object.keys(resp).length < 1) myclient.failure("Something went wrong: " + this.responseText);
                    if (resp["error"] === "no") {
                        myclient.success(resp);
                    } else if (resp["error"] === "yes") {
                        myclient.failure("Something went wrong: " + resp["message"]);
                    } else {
                        myclient.failure("Something went wrong: " + this.responseText);
                    }        
                } catch (err) {
                    myclient.failure(err.message + " - " + this.responseText);
                }
            }
        } catch (err) {
            myclient.failure(err.message);
        }        
    };

    try {
        xhr.open(op_type, url);
        xhr.timeout = time_limit;
        xhr.setRequestHeader("X-CSRFToken", extractToken());
        if (op_type == "POST") {
            const data = new FormData();
            for (ckey in data_dict) {
                data.append(ckey, data_dict[ckey]);
            }
            xhr.send(data);						
        } else {
            xhr.send();						
        }
    }
    catch (err) {
        showCustomAlert(err.message, true);
    }
    return false;
};
// show or hide button for "scroll to top"
// myclient.minHeight is set in the CSS for the "eis-root" DIV
myclient.setTotop = function() {
    const obj = document.querySelector(".eis-root");
    const cval = (obj.clientHeight > myclient.minHeight) ? "block" : "none";
    document.querySelector("#page_bottom").style.display = cval;
};

//////////////////////////////////////// private message

    function primeInit(toid, toname, withReload) {
        document.querySelector("#prime_operation").dataset.re = (withReload == true) ? "yes" : "no";
        document.querySelector("#prime_operation").dataset.toid = toid;
        document.querySelector("#prime_operation").textContent = "New Private Message to " + toname;
        document.querySelector("#prime_text").value = "";
        document.querySelector("#prime_edit").style.display = "block";
    }
    
    function primeClose() {
        document.querySelector("#prime_edit").style.display = "none";
        return false;
    }

    function primeSend() {
        const toid = document.querySelector("#prime_operation").dataset.toid;
        ctext = document.querySelector("#prime_text").value;
        ctext = (typeof(ctext) !== "string") ? "" : ctext.trim();
        if (ctext.length < 10 || ctext.length > 240) {
            showCustomAlert("The message is too short or too long!", true);
            return false;
        }
        
        showCustomAlert("Wait a moment please...", false);
        myclient.success = function(resp) {
            const withReload = document.querySelector("#prime_operation").dataset.re;
            if (withReload == "yes") location.reload(true);
            primeClose();
            hideCustomAlert();
            return false;
        };
        myclient.send( {"toid":toid, "ctext":ctext}, "POST", "/privatemessage", 60000);
        return false;
    }

//////////////////////////////////////// flagger (reporting items - bell icon)

    function flaggerInit(cid, ctype, what) {
        document.querySelector("#flagger_operation").dataset.id = cid;
        document.querySelector("#flagger_operation").dataset.type = ctype;
        document.querySelector("#flagger_operation").textContent = "You are reporting a " + what + ". Please describe the problem!";
        document.querySelector("#flagger_text").value = "";
        document.querySelector("#flagger_edit").style.display = "block";
    }
    
    function flaggerClose() {
        document.querySelector("#flagger_edit").style.display = "none";
        return false;
    }

    function flaggerSend() {
        const cid = document.querySelector("#flagger_operation").dataset.id;
        const ctype = document.querySelector("#flagger_operation").dataset.type;
        let ctext = document.querySelector("#flagger_text").value;
        ctext = (typeof(ctext) !== "string") ? "" : ctext.trim();
        if (ctext.length < 20 || ctext.length > 240) {
            showCustomAlert("The description is too short or too long!", true);
            return false;
        }
        
        showCustomAlert("Wait a moment please...", false);
        myclient.success = function(resp) {
            flaggerClose();
            hideCustomAlert();
            showCustomAlert("Our staff is going to review the problem as soon as possible!", true);
            return false;
        };
        myclient.send( {"ctype":ctype, "cid":cid, "text":ctext}, "POST", "/itemflag", 60000);
        return false;
    }

    /////////////////////////////////////// item delete ("X" icon)
  
    function itemDelete() {
        document.querySelector("#delitem_wait").style.display = "none";
        showCustomAlert("Wait a moment please...", false);
        const cradix = document.querySelector("#delitem_yes").dataset.radix;
        const ctype = document.querySelector("#delitem_yes").dataset.type;
        const cval = document.querySelector("#delitem_yes").dataset.val;
        const aval = cval.split("_");

        myclient.success = function(resp) {
            const cval = document.querySelector("#delitem_yes").dataset.val;
            const ochild = document.querySelector("#" + cradix + cval.substring(2));
            const oparent = document.querySelector("#page_list");
            oparent.removeChild(ochild);
            hideCustomAlert();
            return false;
        };
        myclient.send( {"cid":aval[1], "ctype":ctype}, "POST", "/itemdelete", 60000);
        return false;
    }

////////////////////////////////////////// listeners

document.addEventListener('DOMContentLoaded', function() {
    // close custom alert
    document.querySelector("#mess_tick").onclick = function() {
        hideCustomAlert();
        return false;
    };
        
    // proceed with delete
    document.querySelector("#delitem_yes").onclick = function() {
        itemDelete();
        return false;
    };

    // close delete dialog
    document.querySelector("#delitem_no").onclick = function() {
        document.querySelector("#delitem_wait").style.display = "none";
        return false;
    };
    
    // cancel flagger
    document.querySelector("#flagger_cancel").onclick = function() {
        flaggerClose();
        return false;
    };

    // send new flagger
    document.querySelector("#flagger_ok").onclick = function() {
        flaggerSend();
        return false;
    };
    
    // cancel private message
    document.querySelector("#prime_cancel").onclick = function() {
        primeClose();
        return false;
    };

    // send new private message
    document.querySelector("#prime_ok").onclick = function() {
        primeSend();
        return false;
    };

    // go to top - handling "scroll to top" button
    document.querySelector("#page_bottom").onclick = function() {
        document.querySelector("#page_top").scrollIntoView(false);
        return false;
    };

});
