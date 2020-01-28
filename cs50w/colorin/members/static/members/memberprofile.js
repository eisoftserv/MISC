
function closeNewNetwork() {
    document.querySelector("#new_network").style.display = "none";
}

function newSocial() {  
	let cname = document.querySelector("#new_network_name").value;
	cname = (typeof(cname) === "string") ? cname.trim() : "";
	tx = "";
	if (cname.length < 2 || cname.length > 80) tx = tx + "The value is too short; ";
	if (cname.startsWith("https://") == false) tx = tx + "The URL must start with https://";
	if (tx.length > 0) {
		showCustomAlert(tx, true);
		return false;
	}

	showCustomAlert("Wait a moment please...", false);
	myclient.success = function(resp) {
		closeNewNetwork();
		hideCustomAlert();
		showCustomAlert("Your proposal is going to be reviewed by our staff as soon as possible!", true);
		return false;
	};
	myclient.send({"name":cname, "type":"social"}, "POST", "/membernewplatform", 60000);
	return false;
}

/////////////////////////////// listeners

document.addEventListener('DOMContentLoaded', function() {
	// send new network
	const objo = document.querySelector("#new_network_ok");
	if (objo) {
		objo.onclick = function() {
			newSocial();
			return false;
		};	
	}
	// cancel new network
	const objc = document.querySelector("#new_network_clear");
	if (objc) {
		objc.onclick = function() {
			closeNewNetwork();
			return false;
		};
	}
	// add new network
	const objn = document.querySelector("#menu_network");
	if (objn) {
		objn.onclick = function() {
			document.querySelector("#new_network_name").value = "https://";
			document.querySelector("#new_network").style.display = "block";
			return false;
		};
	}
	// back button
	const objb = document.querySelector("#menu_back");
	if (objb) {
		objb.onclick = function() {
			location.href = "/memberboard";
			return false;
		};
	}
    
	myclient.setTotop();
	
});    
