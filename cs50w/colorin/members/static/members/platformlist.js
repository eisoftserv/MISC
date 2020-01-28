
function closeNewPlatform() {
    document.querySelector("#new_plt").style.display = "none";
}

function newPlatform() {  
    let cname = document.querySelector("#new_plt_name").value;
    cname = (typeof(cname) === "string") ? cname.trim() : "";
    tx = "";
    if (cname.length < 2 || cname.length > 80) tx = tx + "The value is too short; ";
    if (cname.startsWith("https://") == false) tx = tx + "The URL must start with https://";
    if (tx.length > 0) {
        showCustomAlert(tx, true);
        return false;
    }
    // send to server
    showCustomAlert("Wait a moment please...", false);
    myclient.success = function(resp) {
        closeNewPlatform();
        hideCustomAlert();
        showCustomAlert("Your proposal is going to be reviewed by our staff as soon as possible!", true);
        return false;
    };
    myclient.send( {"name":cname, "type":"resource"}, "POST", "/membernewplatform", 60000);
    return false;
}

/////////////////////////////// listeners

document.addEventListener('DOMContentLoaded', function() {
    // click on ...
    const objs = document.querySelectorAll(".eis-platform-link");
    if (objs) {
        objs.forEach(elem => { 
            elem.onclick = function() {
                const cid = this.id.substring(3);
                location.href = "platformdetails/" + cid + "/";
            };
            return false;
        });
    }

    // send new platform
    document.querySelector("#new_plt_ok").onclick = function() {
        newPlatform();
        return false;
    };

    // cancel new platform
    document.querySelector("#new_plt_clear").onclick = function() {
        closeNewPlatform();
        return false;
    };
    
    // add new platform
    document.querySelector("#menu_plt").onclick = function() {
        document.querySelector("#new_plt_name").value = "https://";
        document.querySelector("#new_plt").style.display = "block";
        return false;
    };

    // go to themes
    document.querySelector("#menu_flip").onclick = function() {
        location.href = "/memberboard";
        return false;
    };   
       
    myclient.setTotop();

});    

