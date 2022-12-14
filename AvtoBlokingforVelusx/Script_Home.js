// JavaScript source code
const ipv4 = "169.254.82.150"

function delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}
var masMasks = [];

async function doGetreqvest(url) {
    let response = await fetch(url);
    let data = await response.text();
    //console.log(data);
    return data;
}

async function reqvestLoop(ms) {
    var i = 0;
    console.log("Start");

    var Maskslist = document.getElementById('ListMasks');
    var delayTimeText = document.getElementById('TimeDelayValue');
    var delayTimeRang = document.getElementById('TimeDelayRange');
    var lastScanText = document.getElementById('LastScan');
    var releText = document.getElementById('Rele');
    var timeToChengText = document.getElementById('TimeToCheng');

    let data = await doGetreqvest("http://" + ipv4 + ":8080/Masks");
    masMasks = data.split(";");
    var interTextForMasks = "";
    for (i in masMasks) {
        interTextForMasks = interTextForMasks + "<option>" + masMasks[i] + "</option>";
    }
    Maskslist.innerHTML = interTextForMasks;

    data = await doGetreqvest("http://" + ipv4 + ":8080/DealyTime");
    delayTimeText.innerHTML = data;
    delayTimeRang.setAttribute("value", data);


    setInterval(async function () {
        data = await doGetreqvest("http://" + ipv4 + ":8080/Rele");
        if (data === "OFF") {
            releText.style.background = "red";
        } else {
            releText.style.background = "green";
        }
        releText.innerHTML = data;

        data = await doGetreqvest("http://" + ipv4 + ":8080/TimeToCheng");
        timeToChengText.innerHTML = data + " sec.";

        data = await doGetreqvest("http://" + ipv4 + ":8080/LastScan");
        lastScanText.innerHTML = data;

    }, ms);
}

function updateListOfMasks() {
    var Maskslist = document.getElementById('ListMasks');
    var interTextForMasks = "";
    for (i in masMasks) {
        interTextForMasks = interTextForMasks + "<option>" + masMasks[i] + "</option>";
    }
    Maskslist.innerHTML = interTextForMasks;
}

function removeItem(array, item) {
    for (var i in array) {
        if (array[i] == item) {
            array.splice(i, 1);
            break;
        }
    }
}

async function SaveDataInPost(data, url) {
    var xhr = new XMLHttpRequest();
    xhr.open("POST",url , true);
    xhr.setRequestHeader('Content-Type', 'application/text');
    xhr.send(data);

    xhr.onload = function () {
        var data = this.responseText;
        console.log(data);
    };
}

function PreperDataForSend() {
    var arg1 = "";
    for (i in masMasks) {
        arg1 = arg1 + masMasks[i] + ";";
    }
    arg1 = arg1.substring(0,arg1.length - 1);
    return arg1;
}

function onClicButtonAction(eventObj) {
    var button = eventObj.target;

    var name = button.value;
    switch (name) {
        case "Add":
            var item = document.getElementById("TextMask").value;
            if (item.length != 6) {
                alert("Mask can't be have length not equal 6!");
                break;
            }
            if (!masMasks.includes(item)) {
                masMasks.push(item);
                updateListOfMasks();
                //alert("Mask " + item + " add to array.");
            } else {
                alert("Mask " + item +" is present in array!");
            }
            break;
        case "Remove":
            var item = document.getElementById("TextMask").value;
            if (item.length != 6) {
                alert("Mask can't be have length not equal 6!");
                break;
            }
            if (!masMasks.includes(item)) {
                alert("Mask " + item + " is absent in array!");
                break;
            }
            removeItem(masMasks, item);
            updateListOfMasks();
            document.getElementById("TextMask").value = ""; 
            //alert("Mask " + item +" was remove");
            break;
        case "Save data":
            SaveDataInPost(PreperDataForSend(), "http://" + ipv4 + ":8080/SaveMask"); 
            SaveDataInPost(document.getElementById("TimeDelayRange").value, "http://" + ipv4 + ":8080/SaveTimeDelay");
            alert("Data have been saved and send to server.");
            break;
    }
}
function onClicItemAction() {
    var item = document.getElementById("ListMasks");
    if (typeof (item) != "undefined") {
        document.getElementById("TextMask").value = item.options[item.selectedIndex].value; 
    }   
}
function onScrollAction() {
    var rang = document.getElementById("TimeDelayRange");
    var TimeDelayValueText = document.getElementById("TimeDelayValue");
    TimeDelayValueText.innerHTML = rang.value;
}

function init() {
    //alert("Page is load!");


    var buttons = document.getElementsByClassName("buttom");
    for (var i = 0; i < buttons.length; i++) {
        buttons[i].onclick = onClicButtonAction;
    }

    var rangOfTimeDelay = document.getElementById("TimeDelayRange");
    rangOfTimeDelay.onchange = onScrollAction;

    var MaskItems = document.getElementById("ListMasks");
    MaskItems.onclick = onClicItemAction;

    reqvestLoop(500);
}
window.onload = init;