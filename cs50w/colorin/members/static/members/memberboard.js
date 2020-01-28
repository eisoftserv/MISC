
function closeNewTheme() {
    document.querySelector("#new_theme").style.display = "none";
    return false;
}

function newTheme() {  
    let cname = document.querySelector("#new_theme_name").value;
    cname = (typeof(cname) === "string") ? cname.trim() : "";
    if (cname.length < 2 || cname.length > 80) {
        showCustomAlert("The value is too short or too long!", true);
        return false;
    }

    showCustomAlert("Wait a moment please...", false);
    myclient.success = function(resp) {
        closeNewTheme();
        hideCustomAlert();
        showCustomAlert("Your proposal is going to be reviewed by our staff as soon as possible!", true);
        return false;
    };
    myclient.send( {"name":cname}, "POST", "/membernewtheme", 60000);
    return false;
}

/////////////////////////////// listeners
document.addEventListener('DOMContentLoaded', function() {
    // click on theme
    const objs = document.querySelectorAll(".eis-theme-link");
    if (objs) {
        objs.forEach(elem => { 
            elem.onclick = function() {
                const cid = this.id.substring(3);
                location.href = "themedetails/" + cid + "/";
            };
            return false;
        });
    }
    // send new theme
    document.querySelector("#new_theme_ok").onclick = function() {
        newTheme();
        return false;
    };
    // cancel new theme
    document.querySelector("#new_theme_clear").onclick = function() {
        closeNewTheme();
        return false;
    };
    // add new theme
    document.querySelector("#menu_add").onclick = function() {
        document.querySelector("#new_theme_name").value = "";
        document.querySelector("#new_theme").style.display = "block";
        return false;
    };   
    // go to platforms
    document.querySelector("#menu_flip").onclick = function() {
        location.href = "/platformlist";
        return false;
    };
    myclient.setTotop();
});    
