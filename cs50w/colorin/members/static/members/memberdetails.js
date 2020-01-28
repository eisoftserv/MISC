
document.addEventListener('DOMContentLoaded', function() {
           
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
                location.href = "/commentlist/m/" + this.dataset.oid + "/" + this.dataset.id + "/";               
                return false;
            };
        });
    }
    
    // open private message
    const objmess = document.querySelector(".uni-prime");
    if (objmess) {
        objmess.onclick = function() {
            const obj = document.querySelector("#page_about");        
            primeInit(obj.dataset.id, obj.value, false);
            return false;
        };
    }

    // flag profile
    objflag = document.querySelector(".uni-flax");
    if (objflag) {
        document.querySelector(".uni-flax").onclick = function() {
            flaggerInit(this.dataset.id, "profile", "member profile");
            return false;
        };
    }
        
    myclient.setTotop();

});    
