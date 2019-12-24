			let currentUser = "";
			let currentChannel = "";
			let status = "init";

			// dummy authentication for development purposes only
			function checkCurrentUser() {

				const xhr = new XMLHttpRequest();
				xhr.onreadystatechange = function() {
					try {
						if (this.readyState == 4) {
							if (this.status == 404) {
								if (status === "init") {
									loglocal(false);
									status = "before";
								}
								alert("User " + currentUser + " NOT Found!");
								document.querySelector("#show_signin").style.display = "block";
							} else if (this.status > 199 && this.status < 300) {
								if (status === "init") {
									tx = "Hello " + currentUser + "! Hit 'Cancel' in case you want to log in as a different user!";
									const resp = confirm(tx);
									if (resp !== true) {
										loglocal(false);
										document.querySelector("#name_signin").value = "";
										document.querySelector("#show_signin").style.display = "block";
										status = "before";
									} else {
										status = "olduser";
									}
								} else {
									document.querySelector("#show_signin").style.display = "none";
									status = "newuser";
								}
							} else {
								throw new Error(this.statusText);
							}				

							if (status === "newuser") {
								currentChannel = "";
								loglocal(true);
							}

							if (status === "olduser" || status === "newuser") {
							// navigate to the proper chat page via server endpoint
								location.href = "/chat/" + encodeURIComponent(currentUser);
							}

						}
					} catch (err) {
						document.querySelector("#show_signin").style.display = "none";
						alert(err.message);
					}
				};

				try {
					const data = new FormData();
					data.append("name", currentUser);
					xhr.open("POST", "/checkuser");
					xhr.timeout = 30000;
					xhr.send(data);						
				}
				catch (err) {
					document.querySelector("#show_signin").style.display = "none";
					alert(err.message);
				}

			}


			function loglocal(save) {
				if (save == false) {
					currentChannel = "";
					currentUser = "";
				}
				localStorage.setItem("currentChannel", currentChannel);
				localStorage.setItem("currentUser", currentUser);
			};
			
			//////////////////////////////////////////////////// page load event handler

			document.addEventListener('DOMContentLoaded', function() {
				// sign in
				document.querySelector("#send_signin").onclick = function() {
					try {
						const obj = document.querySelector("#name_signin");
						if (!obj) throw new Error("Error in the input form!");
						let val = obj.value;
						if (!val) throw new Error("Please complete the user name!");
						val = val.trim();
						if (val.length < 2 || val.length > 30) throw new Error("User name should have between 2 and 30 characters!");
						currentUser = val;
						status = "after";
						checkCurrentUser();
					}
					catch (err) {
						alert(err.message);
					}
					// handle auto-submit
					return false;
				};

				// cancel sign in
				document.querySelector("#cancel_signin").onclick = function() {
					if (status === "after") loglocal(false);
					document.querySelector("#show_signin").style.display = "none";
					// handle auto-submit
					return false;
				};

				currentUser = localStorage.getItem('currentUser');
				currentChannel = localStorage.getItem('currentChannel');

				if (typeof currentUser === "string" && currentUser.length > 1) {
					status = "init";
					checkCurrentUser();
				} else {
					status = "before";
					currentUser = "";
					currentChannel = "";
					document.querySelector("#name_signin").value = "";
					document.querySelector("#show_signin").style.display = "block";					
				}

			});
		