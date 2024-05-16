
function rettext(value) {
	if (value) {
		return $('<div/>').text(value).html();
	} else {
		return '';
	}
}

snack_wit = false;
added_snack = [];
snacks = 0;
function snackBar(title , tp="0"){
	if(tp == "1"){
		if(snack_wit == false){
			snack_wit = true;
			document.getElementById("snackbar").removeAttribute("style");
			setTimeout(function(){
				document.getElementById("snackbar").style.bottom="20px";
				document.getElementById("snackbarText").innerHTML = String(rettext(title));
				setTimeout(function(){
					document.getElementById("snackbar").removeAttribute("style");
					snack_wit = false;
					snacks -= 1;
					if(snacks == 0){}
					else{
						otherSnackbar(added_snack[snacks]);
					}
				} , 5000);
			},250);
		}
	}else{
		added_snack.push(String(rettext(title)));
		snacks += 1;
		if(snack_wit == false){
			snack_wit = true;
			document.getElementById("snackbar").removeAttribute("style");
			setTimeout(function(){
				document.getElementById("snackbar").style.bottom="20px";
				document.getElementById("snackbarText").innerHTML = String(rettext(title));
				setTimeout(function(){
					document.getElementById("snackbar").removeAttribute("style");
					snack_wit = false;
					snacks -= 1;
					if(snacks == 0){}
					else{
						otherSnackbar(added_snack[snacks]);
					}
				} , 5000);
			},250);
		}
	}
}
function otherSnackbar(title){
	if(snack_wit == false){
		snack_wit = true;
		document.getElementById("snackbar").removeAttribute("style");
		setTimeout(function(){
			document.getElementById("snackbar").style.bottom="20px";
			document.getElementById("snackbarText").innerHTML = String(title);
			setTimeout(function(){
				document.getElementById("snackbar").removeAttribute("style");
				snack_wit = false;
				snacks -= 1;
				if(snacks <= 0){}
				else{
					snackBar(added_snack[snacks],"1");
				}
			} , 5000);
		},250);
	}
}





$(document).on("submit", "form[data-form]",function(e){
	e.preventDefault();
	this_el = this;
	this_el.style.opacity = ".8";
	var formData = new FormData(this);
	$.ajax({
		url: location.href,
		data: formData,
		type: 'POST',
		dataType: 'json',
		mimeType: 'multipart/form-data',
		contentType: false,
		cache: false,
		processData: false,
		success: function(res) {
			this_el.removeAttribute("style");
			if(res.errtitle == ""){
				location.href = res.nextUrl;
			}else{
				snackBar(res.errtitle);
			}
		},
		error: function(res){
			console.log(res);
		}
	});
});


$(document).on("click","#nav",function(){
	if(document.querySelector("nav").style.height == ""){
		document.querySelector("nav").style.height = "275px";
	}else{
		document.querySelector("nav").removeAttribute("style");
	}
});


$(document).on("click","[data-for]", function(){
	document.getElementById(this.dataset.for).click();
});

objectsCount = 0;
addressesCount = 0;
violationsCount = 0;

$(document).on("change","#object", function(evt){
	objectsCount ++;


	imgCard = document.createElement("div");
	imgCard.className = "img-card";
	imgCard.id = `objectBox${objectsCount}`;
	imgCardBox = document.createElement("div");
	imgCardBox.className = "img-card-box";
	img = document.createElement("img");
	$(imgCardBox).append(img);

	var tgt = evt.target || window.event.srcElement,
      files = tgt.files;

    if (FileReader && files && files.length) {
        var fr = new FileReader();
        fr.onload = function () {
          img.src = fr.result;
        }
        fr.readAsDataURL(files[0]);
    }

	p = document.createElement("p");
	p.innerHTML = document.getElementById("object").value.split("\\").pop();
	button = document.createElement("button");
	button.type = "button";
	button.className = "btn ibtn";
	button.dataset.close = `objectBox${objectsCount}`;
	span = document.createElement("span");
	span.className = "material-symbols-sharp";
	span.innerHTML = "close";
	$(button).append(span);
	$(imgCard).append(imgCardBox);
	$(imgCard).append(p);
	$(imgCard).append(button);
	$(`#objectsImages`).append(imgCard);


	document.getElementById("object").setAttribute('name',`objectBox${objectsCount}`);
	document.getElementById("object").id = `objectBox${objectsCount}`;
	object = document.createElement("input");
	object.type = "file";

	object.accept = "image/*";

	object.setAttribute("hidden","");
	object.id = "object";
	$(`#objectsImages`).append(object);
	imgCard.appendChild(document.getElementById(`objectBox${objectsCount}`));
});


$(document).on("change","#address", function(evt){
	addressesCount ++;


	imgCard = document.createElement("div");
	imgCard.className = "img-card";
	imgCard.id = `addressBox${addressesCount}`;
	imgCardBox = document.createElement("div");
	imgCardBox.className = "img-card-box";
	img = document.createElement("img");
	$(imgCardBox).append(img);

	var tgt = evt.target || window.event.srcElement,
      files = tgt.files;

    if (FileReader && files && files.length) {
        var fr = new FileReader();
        fr.onload = function () {
          img.src = fr.result;
        }
        fr.readAsDataURL(files[0]);
    }

	p = document.createElement("p");
	p.innerHTML = document.getElementById("address").value.split("\\").pop();
	button = document.createElement("button");
	button.type = "button";
	button.className = "btn ibtn";
	button.dataset.close = `addressBox${addressesCount}`;
	span = document.createElement("span");
	span.className = "material-symbols-sharp";
	span.innerHTML = "close";
	$(button).append(span);
	$(imgCard).append(imgCardBox);
	$(imgCard).append(p);
	$(imgCard).append(button);
	$(`#addressesImages`).append(imgCard);


	document.getElementById("address").setAttribute('name',`addressBox${addressesCount}`);
	document.getElementById("address").id = `addressBox${addressesCount}`;
	address = document.createElement("input");
	address.type = "file";

	address.accept = "image/*";

	address.setAttribute("hidden","");
	address.id = "address";
	$(`#addressesImages`).append(address);
	imgCard.appendChild(document.getElementById(`addressBox${addressesCount}`));
});



$(document).on("change","#violation", function(evt){
	violationsCount ++;


	imgCard = document.createElement("div");
	imgCard.className = "img-card";
	imgCard.id = `violationBox${violationsCount}`;
	imgCardBox = document.createElement("div");
	imgCardBox.className = "img-card-box";
	img = document.createElement("img");
	$(imgCardBox).append(img);

	var tgt = evt.target || window.event.srcElement,
      files = tgt.files;

    if (FileReader && files && files.length) {
        var fr = new FileReader();
        fr.onload = function () {
          img.src = fr.result;
        }
        fr.readAsDataURL(files[0]);
    }

	p = document.createElement("p");
	p.innerHTML = document.getElementById("violation").value.split("\\").pop();
	button = document.createElement("button");
	button.type = "button";
	button.className = "btn ibtn";
	button.dataset.close = `violationBox${violationsCount}`;
	span = document.createElement("span");
	span.className = "material-symbols-sharp";
	span.innerHTML = "close";
	$(button).append(span);
	$(imgCard).append(imgCardBox);
	$(imgCard).append(p);
	$(imgCard).append(button);
	$(`#violationsImages`).append(imgCard);


	document.getElementById("violation").setAttribute('name',`violationsBox${violationsCount}`);
	document.getElementById("violation").id = `violationBox${violationsCount}`;
	violation = document.createElement("input");
	violation.type = "file";

	violation.accept = "image/*";

	violation.setAttribute("hidden","");
	violation.id = "violation";
	$(`#violationsImages`).append(violation);
	imgCard.appendChild(document.getElementById(`violationBox${violationsCount}`));
});



$(document).on("click","[data-close]",function(){
	$(`#${this.dataset.close}`).remove();
});