/////////////////////////

let cart = {};
let current = {};
//
let selist = {};
let selmax = 0;
let selcur = 0;
let selprice = 0.0;
let selname = "";
let selnamex = "";
let selpricex = 0.0;
let selquantity = 1;

///////////////////////// functions

function customAlert(message) {    
    document.querySelector("#cart_message").textContent = message;
    document.querySelector("#cart_tick").style.display = "block";
    document.querySelector("#cart_wait").style.display = "block";
}

function extractToken() {
    let token = "";
    const pairs = document.cookie.split(";");
    pairs.forEach( ele => { 
        if (ele.startsWith("csrftoken=")) token = ele.substring(10);
    });
    return token;
}

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
    nodeList.className = "eis-order-list";
    nodeList.id = "order_sub";
    nodeMain.appendChild(nodeList);

    for (ckey in tbl) {
        const n1 = document.createElement("span");
        n1.className = "eis-order-tx";
        n1.textContent = "id:" + tbl[ckey]["id"];
        const n2 = document.createElement("span");
        n2.className = "eis-order-tx";
        n2.textContent = tbl[ckey]["date"];
        const n3 = document.createElement("span");
        n3.className = "eis-order-nr";
        n3.textContent = "$" + tbl[ckey]["val"];
        const n4 = document.createElement("span");
        n4.className = "eis-order-ta";
        n4.textContent = tbl[ckey]["status"];

        nodeList.appendChild(n1);
        nodeList.appendChild(n2);
        nodeList.appendChild(n3);
        nodeList.appendChild(n4);
    }
}

// pulling data for the client's order list
function requestOrderList() {
    const xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
        try {
            if (this.readyState == 4) {
                if (this.status < 200 || this.status > 299) throw new Error(this.statusText);
                const resp = JSON.parse(this.responseText);
                if (typeof(resp) !== "object") throw new Error("Something went wrong: " + this.responseText);
                if (Object.keys(resp).length < 1) throw new Error("There are no results to show");
                paintOrderList(resp);

                document.querySelector("#cart_wait").style.display = "none";
                document.querySelector("#order_pane").style.display = "block";
            }
        } catch (err) {
            customAlert(err.message);
        }        
    };

    try {
        xhr.open("POST", "/clientorderlist", true);
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

// place new order
function sendNewOrder() {
    const xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
        try {
            if (this.readyState == 4) {
                if (this.status < 200 || this.status > 299) throw new Error(this.statusText);
                const resp = JSON.parse(this.responseText);
                if (resp["error"] === "no") {
                    cart = { "0":{"total":0.0, "crt":0} };
                    customAlert("Your Order ID is: " + resp["message"]);
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
        xhr.open("POST", "/neworder", true);
        xhr.timeout = 30000;
        xhr.setRequestHeader("X-CSRFToken", extractToken());
        const data = new FormData();
        data.append("serialcart", JSON.stringify(cart));
        xhr.send(data);						
    }
    catch (err) {
        customAlert(err.message);
    }
}

// display cart content
function paintCart() {
    const nodeMain = document.querySelector("#cart_main");
    if (!nodeMain) return false;

    document.querySelector("#cart_bigtotal").textContent = "$" + cart["0"]["total"].toFixed(2);

    const nodeSub = document.querySelector("#cart_sub");
    if (nodeSub) {
        let obj = nodeMain.removeChild(nodeSub);
        obj = null;
    }
    const nodeList = document.createElement("div");
    nodeList.className = "eis-cart-list";
    nodeList.id = "cart_sub";
    nodeMain.appendChild(nodeList);

    for (key in cart) {
        if (key === "0") continue;
        const n1 = document.createElement("span");
        n1.className = "eis-cart-tex";
        n1.id = "tex" + key;
        let tx = cart[key]["namex"];
        if (tx.length > 0) tx = " - " + tx;
        n1.textContent = cart[key]["name"] + tx;

        const n2 = document.createElement("span");
        n2.className = "eis-cart-nt";
        n2.id = "tot" + key;
        n2.textContent = "$" + cart[key]["total"].toFixed(2);

        const n4 = document.createElement("span");
        n4.className = "eis-cart-nq";
        n4.id = "qua" + key;
        n4.textContent = cart[key]["quantity"].toString();

        const n3 = document.createElement("span");
        n3.className = "eis-cart-del";
        n3.id = "del" + key;
        n3.textContent = "X";
        n3.onclick = function() {
            let ckey = this.id;
            ckey = ckey.substring(3);
            let o1 = document.querySelector("#tex"+ckey);
            
            let lok = confirm("Are you sure you want to remove from the CART the following item: "+o1.textContent+" ?");
            if (lok !== true) return false;

            this.style.display = "none";
            let o2 = document.querySelector("#tot"+ckey);
            let o3 = document.querySelector("#qua"+ckey);
            o1.style.display = "none";
            o2.style.display = "none";
            o3.style.display = "none";
            if (ckey in cart) {
                cart["0"]["total"] = cart["0"]["total"] - cart[ckey]["total"];
                delete cart[ckey];
            }
            document.querySelector("#cart_bigtotal").textContent = "$" + cart["0"]["total"].toFixed(2);
        } // end function definition

        nodeList.appendChild(n1);
        nodeList.appendChild(n4);
        nodeList.appendChild(n2);
        nodeList.appendChild(n3);
    }
}

// show details pane for clicked product
function showProductDetails() { 
    let res = this.dataset.vals.split('_');
    // begin currently selected item details
    current["gid"] = res[0];
    current["gname"] = document.querySelector("#g" + res[0]).textContent;
    current["pid"] = res[1];
    current["pname"] = document.querySelector("#p" + res[0] + "_" + res[1]).textContent;
    current["tid"] = res[2];
    current["tname"] = document.querySelector("#t" + res[1] + "_" + res[2]).textContent;
    current["nparts"] = parseInt(res[3]);
    current["nextras"] = parseInt(res[4]);
    current["price"] = parseFloat(res[5]);
    current["name"] = current["gname"] + ", " + current["pname"];
    if (current["tname"].length > 0) current["name"] = current["name"] + ", " + current["tname"];
    current["namex"] = "";
    current["pricex"] = 0.0;
    current["quantity"] = 1;
    current["total"] = current["price"];
    // end currently selected item details
    selist = {};
    selmax = 0;
    selcur = 0;
    selname = current["name"];
    selprice = current["price"];
    selnamex = current["namex"];    
    selpricex = current["pricex"];
    selquantity = current["quantity"];

    document.querySelector("#prod_name").textContent = current["name"];
    document.querySelector("#prod_price").textContent = "$" + current["price"].toFixed(2);
    document.querySelector("#prod_namex").textContent = current["namex"];
    if (current["nextras"] > 0) {
        document.querySelector("#prod_pricex").textContent = "$" + current["pricex"].toFixed(2);
    } 
    document.querySelector("#prod_quantity").value = current["quantity"].toString();
    document.querySelector("#prod_total").textContent = "$" + current["total"].toFixed(2);

    const objs = document.querySelectorAll(".eis-selecta");
    objs.forEach(elem => { 
        elem.dataset.sel = "n";
        elem.style.backgroundColor = "white";
    });

    let visip = "none";
    let visie = "none";
    if (current["nparts"] > 0) {
        visip = "block";
        selmax = current["nparts"];
    } else if (current["nextras"] > 0) {
        visie = "block";
        selmax = current["nextras"];
    }
    document.querySelector("#prod_pricex").style.display = visie;
    document.querySelector("#prod_parts").style.display = visip;
    document.querySelector("#prod_extras").style.display = visie;

    document.querySelector("#prod_details").style.display = "block";
}

// recalculates price elements and total for the currently selected product
function recalcDetails() {
    selnamex = "";
    selpricex = 0.0;
    for (let ele in selist) {
        if (selnamex.length > 0) selnamex = selnamex + ", ";
        selnamex = selnamex + selist[ele][0];
        selpricex = selpricex + selist[ele][1];
    }

    document.querySelector("#prod_namex").textContent = selnamex;
    document.querySelector("#prod_pricex").textContent = "$" + selpricex.toFixed(2);
    document.querySelector("#prod_total").textContent = "$" + ((selprice + selpricex)*selquantity).toFixed(2);
}

// when a part or extra is selected or deselected
function processAddonSelection() {
    const sel = this.dataset.sel;
    const val = this.dataset.id;
    // deselected item
    if (sel === "y") {
        if (selcur > 0) selcur--;
        if (val in selist) delete selist[val];
        recalcDetails();
        this.dataset.sel = "n";
        this.style.backgroundColor = "white";
        return false;
    }
    // selected item - over limit
    if (selcur >= selmax) {
        customAlert("You can select only " + selmax.toString() + " items from the list!");        
        return false;
    }
    // selected item - within limit
    const price = this.dataset.price;
    selcur++;
    let nr = 0.0;
    try { nr = parseFloat(price);
    } catch (exc) {
        nr = 0.0;
    }
    selist[val] = [this.textContent, nr];
    recalcDetails();
    this.dataset.sel = "y";
    this.style.backgroundColor = "burlywood";
}

///////////////////////// listeners

document.addEventListener('DOMContentLoaded', function() {

    let txt = localStorage.getItem("cart");    
    
    if (typeof(txt === "string" && txt.length > 0)) {
        try {
            cart = JSON.parse(txt);
            if (cart == null || typeof(cart) !== "object") cart = {};
        } catch (err) {
            cart = {};           
        }
    } else {
        cart = {};
    }

    if (Object.keys(cart).length < 1) {
        cart = { "0":{"total":0.0, "crt":0} };
    }

     // product selected
    const objs = document.querySelectorAll(".eis-prod-buy");
    if (objs) {
        objs.forEach(elem => { 
            elem.onclick = showProductDetails;
            return false;
        });
    }

    // addon selected (part or extra)
    const objl = document.querySelectorAll(".eis-selecta");
    if (objl) {
        objl.forEach(elem => { 
            elem.onclick = processAddonSelection;
            return false;
        });
    }

    document.querySelector("#prod_quantity").onchange = function() {
        selquantity = this.value;
        document.querySelector("#prod_total").textContent = "$" + ((selprice + selpricex)*selquantity).toFixed(2);
        return false;
    };

    // selected product added to cart, hide details pane
    document.querySelector("#prod_details_ok").onclick = function() {
        // complete current selection
        current["namex"] = selnamex;
        current["pricex"] = selpricex;
        current["quantity"] = selquantity;
        current["total"] = (current["price"] + selpricex) * selquantity;
        // add to cart
        cart["0"]["crt"] = cart["0"]["crt"] + 1;
        cart["0"]["total"] = cart["0"]["total"] + current["total"];
        let crt = cart["0"]["crt"].toString();

        cart[crt] = {};
        cart[crt]["name"] = current["name"];
        cart[crt]["namex"] = current["namex"];
        cart[crt]["total"] = current["total"];
        cart[crt]["price"] = current["price"];
        cart[crt]["pricex"] = current["pricex"];
        cart[crt]["quantity"] = current["quantity"];
        cart[crt]["gid"] = current["gid"];
        cart[crt]["pid"] = current["pid"];
        cart[crt]["tid"] = current["tid"];
        
        document.querySelector("#prod_details").style.display = "none";
        return false;
    };

    // selected product not added to cart, hide details pane
    document.querySelector("#prod_details_cancel").onclick = function() {
        document.querySelector("#prod_details").style.display = "none";
        return false;
    };
    
    // show cart pane
    document.querySelector("#cart_menu").onclick = function() {
        paintCart();
        document.querySelector("#cart_base").style.display = "block";
        return false;
    };

    // cart checkout
    document.querySelector("#cart_checkout").onclick = function() {
        if (cart["0"]["total"] < 0.01) {
            customAlert("Please place at least an item into your cart!");
            return false;
        }
        document.querySelector("#cart_base").style.display = "none";
        document.querySelector("#cart_confirm_total").textContent = "$" + cart["0"]["total"].toFixed(2);
        document.querySelector("#cart_confirm").style.display = "block";
        return false;
    };

    // cart close
    document.querySelector("#cart_close").onclick = function() {
        document.querySelector("#cart_base").style.display = "none";
        return false;
    };

    // cart send order
    document.querySelector("#cart_send").onclick = function() {
        document.querySelector("#cart_confirm").style.display = "none";
        document.querySelector("#cart_message").textContent = "Please wait, we are placing your order!";
        document.querySelector("#cart_wait").style.display = "block";
        sendNewOrder();
        return false;
    };

    // cart close cofirmation
    document.querySelector("#cart_review").onclick = function() {
        document.querySelector("#cart_confirm").style.display = "none";
        return false;
    };

    // close custom alert
    document.querySelector("#cart_tick").onclick = function() {
        document.querySelector("#cart_wait").style.display = "none";
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
        document.querySelector("#cart_message").textContent = "Please wait, we are grabbing your data!";
        document.querySelector("#cart_wait").style.display = "block";
        requestOrderList();
        return false;
    };
 
});

///////////////////////////////////////

window.addEventListener('beforeunload', function(event) {
    localStorage.setItem("cart", JSON.stringify(cart));
});
