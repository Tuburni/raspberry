window.onload = init;

function init() {
	/*var image = document.getElementById("zero");
	image.onclick = showAnswer;*/
	var images = document.getElementsByTagName('img');
	for(var i = 0; i < images.length; i++){
		images[i].onclick = showAnswer;
	}
}

function showAnswer(eventObj) {
	/*var image = document.getElementById("zero");
	image.src = "img/zero.jpg";*/
	var image = eventObj.target;

	var name = image.id;
	name = "img/" + name + ".jpg";
	image.src = name;
}


//target, type, timeStamp, keyCode, clientX, clientY, touches