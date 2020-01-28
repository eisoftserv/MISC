    
    function cmntInit() {
        const sid = document.querySelector("#page_title").dataset.id;
        document.querySelector("#cmnt_operation").dataset.val = "ci" + sid + "_0";
        document.querySelector("#cmnt_operation").textContent = "Add Comment";
        document.querySelector("#cmnt_text").value = "";
        document.querySelector("#cmnt_edit").style.display = "block";
    }
    
    function cmntClose() {
        document.querySelector("#cmnt_edit").style.display = "none";
        return false;
    }
    
    function cmntPrefill(cval) {
        document.querySelector("#cmnt_operation").dataset.val = cval;
        document.querySelector("#cmnt_operation").textContent = "Edit Comment";
        const coda = cval.substring(2);
        document.querySelector("#cmnt_text").value = document.querySelector("#cc" + coda).textContent;
        document.querySelector("#cmnt_edit").style.display = "block";
    }
    
    function cmntPostfill() {
        const coda = document.querySelector("#cmnt_operation").dataset.val.substring(2);
        document.querySelector("#cc" + coda).textContent = document.querySelector("#cmnt_text").value;
    }

    ////////////////////////////////////////

    function updateComment() {
        const str_id = document.querySelector("#cmnt_operation").dataset.val.substring(2);
        const avals = str_id.split("_");
        const sid = avals[0];
        const cid = avals[1];
        ctext = document.querySelector("#cmnt_text").value;
        ctext = (typeof(ctext) !== "string") ? "" : ctext.trim();
        if (ctext.length < 10) {
            showCustomAlert("The comment is too short!", true);
            return false;
        }

        showCustomAlert("Wait a moment please...", false);
        myclient.success = function(resp) {
            if (resp["old"] == "0") {
                location.reload(true);
            } else {
                cmntPostfill();
            }
            cmntClose();
            hideCustomAlert();
            return false;
        };
        myclient.send( {"sid":sid, "cid":cid, "text":ctext}, "POST", "/commentrecord", 60000);
        return false;
    }
   
    /////////////////////////////// listeners
    
    document.addEventListener('DOMContentLoaded', function() {
        
        const obje = document.querySelectorAll(".uni-edit");
        if (obje) {
            obje.forEach(elem => { 
                elem.onclick = function() {
                    cmntPrefill(this.id);
                    return false;
                };
            });
        }
        
        const objd = document.querySelectorAll(".uni-dele");
        if (objd) {
            objd.forEach(elem => { 
                elem.onclick = function() {
                    document.querySelector("#delitem_message").textContent = "Are you sure you want to hide your comment?";
                    document.querySelector("#delitem_yes").dataset.val = this.id;
                    document.querySelector("#delitem_yes").dataset.radix = "cx";
                    document.querySelector("#delitem_yes").dataset.type = "comment";
                    document.querySelector("#delitem_wait").style.display = "block";
                    return false;
                };
            });
        }
        
        const objf = document.querySelectorAll(".uni-flag");
        if (objf) {
            objf.forEach(elem => { 
                elem.onclick = function() {
                    flaggerInit(this.dataset.id, "comment", "comment");
                    return false;
                };
            });
        }

        // insert
        document.querySelector("#menu_add").onclick = function() {
            cmntInit();
            return false;
        };
    
        // cancel edit
        document.querySelector("#cmnt_cancel").onclick = function() {
            cmntClose();
            return false;
        };
    
        // send new comment
        document.querySelector("#cmnt_ok").onclick = function() {
            updateComment();
            return false;
        };
    
        // back button
        document.querySelector("#menu_back").onclick = function() {
            const obj = document.querySelector("#page_title");
            const ctype = obj.dataset.ctype;
            if (ctype == "t") location.href = "/themedetails/" + obj.dataset.oid + "/";
            if (ctype == "p") location.href = "/platformdetails/" + obj.dataset.oid + "/";
            if (ctype == "m") location.href = "/memberdetails/" + obj.dataset.oid + "/";
            return false;
        };

        myclient.setTotop();
        
    });    
    