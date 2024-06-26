
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
				document.getElementById("snackbarText").textContent = title;
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
				document.getElementById("snackbarText").textContent = title;
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
			document.getElementById("snackbarText").textContent = title;
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
			snackBar("حدث خطأ اثناء الحفظ !");
		}
	});
});


$(document).on("click","#nav",function(){
	if(document.querySelector("nav").style.height == ""){
		if($('#userRole').val() == "admin"){
			document.querySelector("nav").style.height = "340px";
		}else{
			document.querySelector("nav").style.height = "300px";
		}
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

objectsCountE = 0;
addressesCountE = 0;
violationsCountE = 0;

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
	p.textContent = document.getElementById("object").value.split("\\").pop();
	button = document.createElement("button");
	button.type = "button";
	button.className = "btn ibtn";
	button.dataset.close = `objectBox${objectsCount}`;
	span = document.createElement("span");
	span.className = "material-symbols-sharp";
	span.textContent = "close";
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
	p.textContent = document.getElementById("address").value.split("\\").pop();
	button = document.createElement("button");
	button.type = "button";
	button.className = "btn ibtn";
	button.dataset.close = `addressBox${addressesCount}`;
	span = document.createElement("span");
	span.className = "material-symbols-sharp";
	span.textContent = "close";
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
	p.textContent = document.getElementById("violation").value.split("\\").pop();
	button = document.createElement("button");
	button.type = "button";
	button.className = "btn ibtn";
	button.dataset.close = `violationBox${violationsCount}`;
	span = document.createElement("span");
	span.className = "material-symbols-sharp";
	span.textContent = "close";
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

	textField = document.createElement("textarea");
	textField.setAttribute("name",`note${violationsCount}`);
	textField.setAttribute("id",`note${violationsCount}`);
	textField.setAttribute("placeholder",`وصف المخالفة`);
	textField.className = "note";
	$("#violationsImages").append(textField);
	imgCard.appendChild(document.getElementById(`violationBox${violationsCount}`));
});




$(document).on("change","#objectE", function(evt){
	objectsCountE ++;


	imgCard = document.createElement("div");
	imgCard.className = "img-card";
	imgCard.id = `objectBoxE${objectsCountE}`;
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
	p.textContent = document.getElementById("objectE").value.split("\\").pop();
	button = document.createElement("button");
	button.type = "button";
	button.className = "btn ibtn";
	button.dataset.close = `objectBoxE${objectsCountE}`;
	span = document.createElement("span");
	span.className = "material-symbols-sharp";
	span.textContent = "close";
	$(button).append(span);
	$(imgCard).append(imgCardBox);
	$(imgCard).append(p);
	$(imgCard).append(button);
	$(`#objectsImagesE`).append(imgCard);


	document.getElementById("objectE").setAttribute('name',`objectBoxE${objectsCountE}`);
	document.getElementById("objectE").id = `objectBoxE${objectsCountE}`;
	object = document.createElement("input");
	object.type = "file";

	object.accept = "image/*";

	object.setAttribute("hidden","");
	object.id = "objectE";
	$(`#objectsImagesE`).append(object);
	imgCard.appendChild(document.getElementById(`objectBoxE${objectsCountE}`));
});


$(document).on("change","#addressE", function(evt){
	addressesCountE ++;


	imgCard = document.createElement("div");
	imgCard.className = "img-card";
	imgCard.id = `addressBoxE${addressesCountE}`;
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
	p.textContent = document.getElementById("addressE").value.split("\\").pop();
	button = document.createElement("button");
	button.type = "button";
	button.className = "btn ibtn";
	button.dataset.close = `addressBoxE${addressesCountE}`;
	span = document.createElement("span");
	span.className = "material-symbols-sharp";
	span.textContent = "close";
	$(button).append(span);
	$(imgCard).append(imgCardBox);
	$(imgCard).append(p);
	$(imgCard).append(button);
	$(`#addressesImagesE`).append(imgCard);


	document.getElementById("addressE").setAttribute('name',`addressBoxE${addressesCountE}`);
	document.getElementById("addressE").id = `addressBoxE${addressesCountE}`;
	address = document.createElement("input");
	address.type = "file";

	address.accept = "image/*";

	address.setAttribute("hidden","");
	address.id = "addressE";
	$(`#addressesImagesE`).append(address);
	imgCard.appendChild(document.getElementById(`addressBoxE${addressesCountE}`));
});



$(document).on("change","#violationE", function(evt){
	violationsCountE ++;


	imgCard = document.createElement("div");
	imgCard.className = "img-card";
	imgCard.id = `violationBoxE${violationsCountE}`;
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
	p.textContent = document.getElementById("violationE").value.split("\\").pop();
	button = document.createElement("button");
	button.type = "button";
	button.className = "btn ibtn";
	button.dataset.close = `violationBoxE${violationsCountE}`;
	span = document.createElement("span");
	span.className = "material-symbols-sharp";
	span.textContent = "close";
	$(button).append(span);
	$(imgCard).append(imgCardBox);
	$(imgCard).append(p);
	$(imgCard).append(button);
	$(`#violationsImagesE`).append(imgCard);


	document.getElementById("violationE").setAttribute('name',`violationsBoxE${violationsCountE}`);
	document.getElementById("violationE").id = `violationBoxE${violationsCountE}`;
	violation = document.createElement("input");
	violation.type = "file";

	violation.accept = "image/*";

	violation.setAttribute("hidden","");
	violation.id = "violationE";
	$(`#violationsImagesE`).append(violation);

	textField = document.createElement("textarea");
	textField.setAttribute("name",`noteE${violationsCountE}`);
	textField.setAttribute("id",`noteE${violationsCountE}`);
	textField.setAttribute("placeholder",`وصف المخالفة`);
	textField.className = "noteE";
	$("#violationsImagesE").append(textField);
	imgCard.appendChild(document.getElementById(`violationBoxE${violationsCountE}`));
});



$(document).on("click","[data-close]",function(){
	$(`#${this.dataset.close}`).remove();
	noteId =  this.dataset.close.replace("violationBoxE","")
		.replace("violationBox","")
		.replace("addressBoxE","")
		.replace("addressBox","")
		.replace("objectBoxE","")
		.replace("objectBox","");
	$(`#note${noteId}`).remove();
});

function orderForm(){
	this_el = document.getElementById("addOrderForm");
	this_el.style.opacity = ".8";
	var formData = new FormData(this_el);
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
			snackBar("حدث خطأ اثناء الحفظ !");
		}
	});
}

function orderFormE(){
	this_el = document.getElementById("editOrderForm");
	this_el.style.opacity = ".8";
	var formData = new FormData(this_el);
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
			snackBar("حدث خطأ اثناء الحفظ !");
		}
	});
}

$(document).on("click","#saveBtn", function(){
	document.getElementById("isArchive").value = "no";
	orderForm();
	// document.getElementById("addOrderForm").submit();
});

$(document).on("click","#archiveBtn", function(){
	document.getElementById("isArchive").value = "yes";
	orderForm();
});


$(document).on("click","#saveBtnE", function(){
	document.getElementById("isArchiveE").value = "no";
	orderFormE();
	// document.getElementById("addOrderForm").submit();
});

$(document).on("click","#archiveBtnE", function(){
	document.getElementById("isArchiveE").value = "yes";
	orderFormE();
});

$(document).on("click", "#delete", function(){
	location.href = rettext(`/delete/${document.getElementById("orderNum").textContent}`);
});

$(document).on("click", "#export", function(){
	location.href = rettext(`/export/${document.getElementById("orderNum").textContent}`);
});

$(document).on("click", ".list > button", function(){
	this_el = this;
	$.ajax({
		url: location.href,
		data: {
			pk: this.dataset.order,
			getOrder:""
		},
		type: 'GET',
		dataType: 'json',
		success: function(res) {
			if(this_el.dataset.type == "home"){
				document.getElementById("orderNum").textContent = res.data[1];
				document.getElementById("orderType").textContent = res.data[2];
				document.getElementById("contractor").textContent = res.data[3];
				document.getElementById("distract").textContent = res.data[4];
				document.getElementById("materials").value = res.data[6];
				res.objects.forEach(image => {
					$("#objectsImages").append(`
						<div class="img-card img-card-2">
							<div class="img-card-box">
								<img src="${rettext(image[0])}">
							</div>
							<p>${rettext(image[2])}</p>
						</div>
					`);
				});
				res.addresses.forEach(image => {
					$("#objectsImages").append(`
						<div class="img-card img-card-2">
							<div class="img-card-box">
								<img src="${rettext(image[0])}">
							</div>
							<p>${rettext(image[2])}</p>
						</div>
					`);
				});
				res.violations.forEach(image => {
					$("#objectsImages").append(`
						<div class="img-card img-card-2">
							<div class="img-card-box">
								<img src="${rettext(image[0])}">
							</div>
							<p>${rettext(image[2])}</p>
						</div>
					`);
				});
			}else{
				document.getElementById("orderNumE").value = res.data[1];
				document.getElementById("contractorE").value = res.data[3];
				document.getElementById("distractE").value = res.data[4];
				try{
					document.getElementById("orderPK").value = res.data[0];
					document.getElementById("orderTypeE").value = res.data[2];
					document.getElementById("materialsE").value = res.data[6];
				}catch{}
				if(res.data[5]){
					document.getElementById("check1").checked = true;
					$("#violationConditionE").val("yes");
					document.getElementById("violationsContainerE").style.display = "block";
				}
				res.objects.forEach(image => {
					$("#objectsImagesE").append(`
						<div class="img-card" id="objectBoxE${rettext(image[1])}">
							<div class="img-card-box">
								<img src="${rettext(image[0])}">
							</div>
							<p>${rettext(image[2])}</p>
							<button type="button" class="btn ibtn" data-close="objectBoxE${rettext(image[1])}"><span class="material-symbols-sharp">close</span></button>
							<input type="file" id="objectBoxE${rettext(image[1])}" accept="image/*" hidden="" name="objectBoxE${rettext(image[1])}">
						</div>
					`);
					if(image[1] >= objectsCountE){
						objectsCountE = image[1] + 1;
					}
				});

				res.addresses.forEach(image => {
					$("#addressesImagesE").append(`
						<div class="img-card" id="addressBoxE${rettext(image[1])}">
							<div class="img-card-box">
								<img src="${rettext(image[0])}">
							</div>
							<p>${rettext(image[2])}</p>
							<button type="button" class="btn ibtn" data-close="addressBoxE${rettext(image[1])}"><span class="material-symbols-sharp">close</span></button>
							<input type="file" id="addressBoxE${rettext(image[1])}" accept="image/*" hidden="" name="addressBoxE${rettext(image[1])}">
						</div>
					`);
					
					if(image[1] >= addressesCountE){
						addressesCountE = image[1] + 1
					}
				});

				res.violations.forEach(image => {
					$("#violationsImagesE").append(`
						<div class="img-card" id="violationBoxE${rettext(image[1])}">
							<div class="img-card-box">
								<img src="${rettext(image[0])}">
							</div>
							<p>${rettext(image[2])}</p>
							<button type="button" class="btn ibtn" data-close="violationBoxE${rettext(image[1])}"><span class="material-symbols-sharp">close</span></button>
							<input type="file" id="violationBoxE${rettext(image[1])}" accept="image/*" hidden="" name="violationBoxE${rettext(image[1])}">
						</div>
						<textarea name="noteE${rettext(image[1])}" id="note${rettext(image[1])}" placeholder="وصف المخالفة" class="note">${rettext(image[3])}</textarea>
					`);
					
					if(image[1] >= violationsCountE){
						violationsCountE = image[1] + 1;
					}
				});
			}
		},
		error: function(res){
			snackBar("حدث خطأ اثناء الحفظ !");
		}
	});
});


$(document).on("click",".close-btn", function(){
	document.getElementById('switch1').style.marginLeft='-200%';
	
	objectsCount = 0;
	addressesCount = 0;
	violationsCount = 0;

	objectsCountE = 0;
	addressesCountE = 0;
	violationsCountE = 0;

	$("#objectsImagesE").empty();
	$("#addressesImagesE").empty();
	$("#violationsImagesE").empty();
});

$(document).on("change", "#orderTypeE", function(){
	if(this.value == "طوارئ"){
		document.querySelector("[name='orderNumE']").placeholder = "رقم العطل"
	}
	else if(this.value == "إحلال" || this.value == "التعزيز" || this.value == "الجهد المتوسط"){
		document.querySelector("[name='orderNumE']").placeholder = "رقم العمل"
	}
});

$(document).on("change", "[name='orderType']", function(){
	if(this.value == "طوارئ"){
		document.querySelector("[name='orderNum']").placeholder = "رقم العطل"
	}
	else if(this.value == "إحلال" || this.value == "التعزيز" || this.value == "الجهد المتوسط"){
		document.querySelector("[name='orderNum']").placeholder = "رقم العمل"
	}
});