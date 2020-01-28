    
    function closeTriDetail() {
        document.querySelector("#new_tri").style.display = "none";
        return false;
    }   

    // send to server
    function manageTri(status) {   
        const obj = document.querySelector("#new_tri_name");
        const ctype = obj.dataset.type;
        const cid = obj.dataset.id.substring(2);
        let cname = obj.value;
        cname = (typeof(cname) === "string") ? cname.trim() : "";
        if (cname.endsWith("/") || cname.endsWith("\\")) cname = cname.substring(0, cname.length - 1);
        tx = "";
        if (cname.length < 2 || cname.length > 80) tx = tx + "The value is too short or too long; ";
        if (ctype != "theme" && cname.startsWith("https://") == false) tx = tx + "The URL must start with https://";
        if (tx.length > 0) {
            showCustomAlert(tx, true);
            return false;
        }
        showCustomAlert("Wait a moment please...", false);
        myclient.success = function(resp) {
            closeTriDetail();
            const cid = document.querySelector("#new_tri_name").dataset.id;
            const obj = document.querySelector("#" + cid);
            obj.dataset.status = "n";
            obj.style.color = "#dfdfdf";
            hideCustomAlert();
            return false;
        };
        if (ctype == "theme") {
            myclient.send( {"cid":cid, "name":cname, "status":status}, "POST", "/staffapprovetheme", 60000);
        } else {
            myclient.send( {"cid":cid, "name":cname, "status":status, "type":ctype}, "POST", "/staffapproveplatform", 60000);
        }
        return false;
    }
    
    /////////////////////////////// listeners
    
    document.addEventListener('DOMContentLoaded', function() {
        // click on theme
        const objt = document.querySelectorAll(".eis-theme-link");
        if (objt) {
            objt.forEach(elem => { 
                elem.onclick = function() {
                    if (this.dataset.status === "n") return false;
                    document.querySelector("#new_tri_title").textContent = "Theme Proposal";                    
                    const obj = document.querySelector("#new_tri_name");
                    obj.value = this.textContent;
                    obj.dataset.id = this.id;
                    obj.dataset.type = "theme";
                    document.querySelector("#new_tri").style.display = "block";
                };
                return false;
            });
        }

        // click on platform
        const objp = document.querySelectorAll(".eis-plt-link");
        if (objp) {
            objp.forEach(elem => { 
                elem.onclick = function() {
                    if (this.dataset.status === "n") return false;
                    document.querySelector("#new_tri_title").textContent = "Platform Proposal";                    
                    const obj = document.querySelector("#new_tri_name");
                    obj.value = this.textContent;
                    obj.dataset.id = this.id;
                    obj.dataset.type = "resource";
                    document.querySelector("#new_tri").style.display = "block";
                };
                return false;
            });
        }
    
        // click on social network
        const objn = document.querySelectorAll(".eis-network-link");
        if (objn) {
            objn.forEach(elem => { 
                elem.onclick = function() {
                    if (this.dataset.status === "n") return false;
                    document.querySelector("#new_tri_title").textContent = "Social Network Proposal";                    
                    const obj = document.querySelector("#new_tri_name");
                    obj.value = this.textContent;
                    obj.dataset.id = this.id;
                    obj.dataset.type = "social";
                    document.querySelector("#new_tri").style.display = "block";
                };
                return false;
            });
        }
    
        // publish tri
        document.querySelector("#new_tri_approve").onclick = function() {
            manageTri("public");
            return false;
        };
    
        // archive tri
        document.querySelector("#new_tri_archive").onclick = function() {
            manageTri("archived");
            return false;
        };
    
        // cancel tri
        document.querySelector("#new_tri_close").onclick = function() {
            closeTriDetail();
            return false;
        };  
         
        myclient.setTotop();

    });    
    