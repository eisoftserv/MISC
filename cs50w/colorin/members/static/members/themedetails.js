
function sugInit() {
    const tid = document.querySelector("#page_title").dataset.id;
    document.querySelector("#sug_operation").dataset.val = "mi" + tid + "_0";
    document.querySelector("#sug_operation").textContent = "Propose Study Material";
    document.querySelector("#sug_title").value = "";
    document.querySelector("#sug_author").value = "";
    document.querySelector("#sug_year").value = "";
    document.querySelector("#sug_url").value = "https://";
    document.querySelector("#sug_text").value = "";
    document.querySelector("#sug_edit").style.display = "block";
}

function sugClose() {
    document.querySelector("#sug_edit").style.display = "none";
    return false;
}

function sugPrefill(cval) {
    document.querySelector("#sug_operation").dataset.val = cval;
    document.querySelector("#sug_operation").textContent = "Edit Proposed Study Material";
    const coda = cval.substring(2);
    document.querySelector("#sug_title").value = document.querySelector("#st" + coda).textContent;
    document.querySelector("#sug_author").value = document.querySelector("#sa" + coda).textContent;
    document.querySelector("#sug_year").value = document.querySelector("#sy" + coda).textContent;
    document.querySelector("#sug_url").value = document.querySelector("#sl" + coda).textContent;
    document.querySelector("#sug_text").value = document.querySelector("#so" + coda).textContent;
    document.querySelector("#sug_edit").style.display = "block";
}

function sugPostfill() {
    const coda = document.querySelector("#sug_operation").dataset.val.substring(2);
    document.querySelector("#st" + coda).textContent = document.querySelector("#sug_title").value;
    document.querySelector("#sa" + coda).textContent = document.querySelector("#sug_author").value;
    document.querySelector("#sy" + coda).textContent = document.querySelector("#sug_year").value;
    document.querySelector("#sl" + coda).textContent = document.querySelector("#sug_url").value;
    document.querySelector("#so" + coda).textContent = document.querySelector("#sug_text").value;
}

function checkYear(cval) {
    if (cval.length < 1) return true;
    if (cval.length < 4) return false;
    if (cval.length > 4) return false;
    nval = parseInt(cval);
    if (isNaN(nval) == true) return false;
    if (nval < 1000) return false;
    curr = new Date();
    ncur = curr.getFullYear();
    if (nval > ncur) return false;
    return true;
}

function checkUrl(cval) {
    if (cval.length < 11) return ("The URL is too short!");
    if (cval.startsWith("https://") == false) return ("The URL must start with https://");
    n1 = cval.indexOf(".", 8);
    if (n1 <= 0) return ("malformed URL");
    n2 = cval.indexOf("/", n1+1);
    if (n2 <= 0) return ("malformed URL");
    return "";
}

function updateSuggestion() {
    const str_id = document.querySelector("#sug_operation").dataset.val.substring(2);
    const avals = str_id.split("_");
    let tx = "";
    title = document.querySelector("#sug_title").value.trim();
    if (title.length < 2) tx = tx + "Title too short; ";
    author = document.querySelector("#sug_author").value.trim();
    cyear = document.querySelector("#sug_year").value.trim();
    if (checkYear(cyear) == false) tx = tx + "incorrect year; ";
    url = document.querySelector("#sug_url").value.trim();
    ctx = checkUrl(url);
    if (ctx.length > 0) {
        tx = tx + ctx + "; ";
    } else {
        if (url.endsWith("/") || url.endsWith("\\")) url = url.substring(0, url.length - 1);
    }
    if (tx.length > 0) {
        showCustomAlert(tx, true);
        return false;
    }
    ctext = document.querySelector("#sug_text").value;
    ctext = (typeof(ctext) !== "string") ? "" : ctext.trim();
    if (tx.length > 0) {
        showCustomAlert(tx, true);
        return false;
    }
    
    showCustomAlert("Wait a moment please...", false);
    myclient.success = function(resp) {
        if (resp["old"] == "0") {
            location.reload(true);
        } else {
            sugPostfill();
        }
        sugClose();
        hideCustomAlert();
        return false;
    };
    myclient.send( {"sid":avals[1], "tid":avals[0], "text":ctext, "title":title, "author":author, "year":cyear, "url":url}, "POST", "/suggestionrecord", 60000);
    return false;
}

/////////////////////////////// listeners

document.addEventListener('DOMContentLoaded', function() {
    
    const obje = document.querySelectorAll(".uni-edit");
    if (obje) {
        obje.forEach(elem => { 
            elem.onclick = function() {
                sugPrefill(this.id);
                return false;
            };
        });
    }
    
    const objd = document.querySelectorAll(".uni-dele");
    if (objd) {
        objd.forEach(elem => { 
            elem.onclick = function() {
                document.querySelector("#delitem_message").textContent = "Are you sure you want to hide your suggestion?";
                document.querySelector("#delitem_yes").dataset.val = this.id;
                document.querySelector("#delitem_yes").dataset.radix = "sx";
                document.querySelector("#delitem_yes").dataset.type = "suggestion";
                document.querySelector("#delitem_wait").style.display = "block";
                return false;
            };
        });
    }
    
    const objf = document.querySelectorAll(".uni-flag");
    if (objf) {
        objf.forEach(elem => { 
            elem.onclick = function() {
                flaggerInit(this.dataset.id, "suggestion", "study material");
                return false;
            };
        });
    }
    
    const objc = document.querySelectorAll(".uni-comm");
    if (objc) {
        objc.forEach(elem => { 
            elem.onclick = function() {
                location.href = "/commentlist/t/" + this.dataset.oid + "/" + this.dataset.id + "/";               
                return false;
            };
        });
    }
    
    // insert
    document.querySelector("#menu_add").onclick = function() {
        sugInit();
        return false;
    };

    // cancel edit
    document.querySelector("#sug_cancel").onclick = function() {
        sugClose();
        return false;
    };

    // send new suggestion
    document.querySelector("#sug_ok").onclick = function() {
        updateSuggestion();
        return false;
    };
           
    myclient.setTotop();

});    
