/////////////////////////

const ostatus = {"id":"", "initial":"", "current":"", currentid:"", "nocolor":"#ffffff", "yescolor":"burlywood"};
ostatus.list = ["placed", "completed", "on-hold", "canceled"];

///////////////////////// functions

function customAlert(message) {    
    document.querySelector("#mess_message").textContent = message;
    document.querySelector("#mess_tick").style.display = "block";
    document.querySelector("#mess_wait").style.display = "block";
}

function extractToken() {
    let token = "";
    const pairs = document.cookie.split(";");
    pairs.forEach( ele => { 
        if (ele.startsWith("csrftoken=")) token = ele.substring(10);
    });
    return token;
}

// send new status
function manageNewStatus() {
    const xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
        try {
            if (this.readyState == 4) {
                if (this.status < 200 || this.status > 299) throw new Error(this.statusText);
                const resp = JSON.parse(this.responseText);
                if (typeof(resp) !== "object" || Object.keys(resp).length < 1) throw new Error("Something went wrong: " + this.responseText);
                if (resp["error"] === "no") {
                    document.querySelector("#" + ostatus.id).textContent = ostatus.current;
                    document.querySelector("#mess_wait").style.display = "none";
                } else if (resp["error"] === "yes") {
                    throw new Error("Something went wrong: " + resp["message"]);
                } else {
                    throw new Error("Something went wrong: " + this.responseText);
                }
            }
        } catch (err) {
            customAlert(err.message);
        }        
    };

    try {
        xhr.open("POST", "/stafforderstatus", true);
        xhr.timeout = 60000;
        xhr.setRequestHeader("X-CSRFToken", extractToken());
        const data = new FormData();
        data.append("id", parseInt(ostatus.id.substring(2)));
        data.append("status", ostatus.current);
        xhr.send(data);						
    }
    catch (err) {
        customAlert(err.message);
    }
} // end function

// order list - client view
function paintOrderList(tbl) {
    const nodeMain = document.querySelector("#order_main");
    if (!nodeMain) return false;

    const nodeSub = document.querySelector("#order_sub");
    if (nodeSub) {
        let obj = nodeMain.removeChild(nodeSub);
        obj = null;
    }
    const nodeList = document.createElement("div");
    nodeList.id = "order_sub";
    nodeMain.appendChild(nodeList);

    for (ckey in tbl) {
        const nhead = document.createElement("div");
        nhead.className = "eis-order-flex";   

        const n1 = document.createElement("span");
        n1.className = "eis-oclient";
        n1.textContent = tbl[ckey]["client"];        
        const n2 = document.createElement("span");
        n2.className = "eis-oid";
        n2.textContent = "id: " + ckey;
        const n3 = document.createElement("span");
        n3.className = "eis-ostamp";
        n3.textContent = tbl[ckey]["stamp"];
        const n4 = document.createElement("span");
        n4.className = "eis-ototal";
        n4.textContent = "$" + tbl[ckey]["total"];

        const n5 = document.createElement("span");
        n5.id = "st" + ckey;
        n5.className = "eis-ostatus";
        n5.textContent = tbl[ckey]["status"];
        n5.onclick = function() {
            ostatus.id = this.id;
            ostatus.initial = this.textContent;
            ostatus.current = ostatus.initial;
            const objs = document.querySelectorAll(".eis-status-option");
            objs.forEach( elem => {
                if (elem.textContent === ostatus.current) {
                    elem.style.backgroundColor = ostatus.yescolor;
                    ostatus.currentid = elem.id;
                } else {
                    elem.style.backgroundColor = ostatus.nocolor;
                }
            });
            document.querySelector("#status_orderid").textContent = this.id.substring(2);
            document.querySelector("#status_pane").style.display = "block";
        };

        nhead.appendChild(n2);
        nhead.appendChild(n1);
        nhead.appendChild(n5);
        nhead.appendChild(n3);
        nhead.appendChild(n4);
        nodeList.appendChild(nhead);

        tbl[ckey]["list"].forEach( elem => {
            const ndetail = document.createElement("div");
            ndetail.className = "eis-order-flex";

            const nm = document.createElement("span");
            nm.className = "eis-oname";
            nm.textContent = elem["n"];
            const np = document.createElement("span");
            np.className = "eis-oprice";
            np.textContent = "$" + elem["p"];
            const nq = document.createElement("span");
            nq.className = "eis-oquantity";
            nq.textContent = elem["q"];

            ndetail.appendChild(nm);
            ndetail.appendChild(nq);
            ndetail.appendChild(np);
            nodeList.appendChild(ndetail);
        });

        nodeList.appendChild(document.createElement("hr"));
    }
} // end function

// pulling data for the client's order list
function requestOrderList() {
    const xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
        try {
            if (this.readyState == 4) {
                if (this.status < 200 || this.status > 299) throw new Error(this.statusText);
                const resp = JSON.parse(this.responseText);
                if (typeof(resp) !== "object") throw new Error("Something went wrong: " + this.responseText);
                if (Object.keys(resp).length < 1) throw new Error("There are no results to show!");
                paintOrderList(resp);
                document.querySelector("#mess_wait").style.display = "none";
                document.querySelector("#order_pane").style.display = "block";
            }
        } catch (err) {
            customAlert(err.message);
        }        
    };

    try {
        xhr.open("POST", "/stafforderlist", true);
        xhr.timeout = 60000;
        xhr.setRequestHeader("X-CSRFToken", extractToken());
        const data = new FormData();
        data.append("filter", "all");
        xhr.send(data);						
    }
    catch (err) {
        customAlert(err.message);
    }
}

///////////////////////// listeners

document.addEventListener('DOMContentLoaded', function() {
    // adding order status list to the DOM
    const omain = document.querySelector("#status_options");
    for (let pos = 0; pos < ostatus.list.length; pos++) {
        const ndiv = document.createElement("div");
        ndiv.id = "op" + pos.toString();
        ndiv.className = "eis-status-option";
        ndiv.textContent = ostatus.list[pos];
        ndiv.onclick = function() {
            if (this.id !== ostatus.currentid) {
                const oldobj = document.querySelector("#" + ostatus.currentid);
                oldobj.style.backgroundColor = ostatus.nocolor;
                ostatus.currentid = this.id;
                ostatus.current = this.textContent;
                this.style.backgroundColor = ostatus.yescolor;
            }
            return false;
        };
        omain.appendChild(ndiv);
    }

    // close custom alert
    document.querySelector("#mess_tick").onclick = function() {
        document.querySelector("#mess_wait").style.display = "none";
        this.style.display = "none";
        return false;
    };

    // close orders list
    document.querySelector("#order_close").onclick = function() {
        document.querySelector("#order_pane").style.display = "none";
        return false;
    };

    // navigate - display orders
    document.querySelector("#orders_menu").onclick = function() {
        document.querySelector("#mess_message").textContent = "Please wait, we are grabbing your data!";
        document.querySelector("#mess_wait").style.display = "block";
        requestOrderList();
        return false;
    };

    // manage status selection
    document.querySelector("#status_pane_ok").onclick = function() {
        if (ostatus.initial !== ostatus.current) {
            document.querySelector("#status_pane").style.display = "none";    
            document.querySelector("#mess_message").textContent = "Please wait, we are updating the database!";
            document.querySelector("#mess_wait").style.display = "block";
            manageNewStatus();
        }
        document.querySelector("#status_pane").style.display = "none";    
        return false;
    };

    // close status selection
    document.querySelector("#status_pane_cancel").onclick = function() {
        document.querySelector("#status_pane").style.display = "none";
        return false;
    };
 
});
