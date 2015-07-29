function sad() {
  alert("I'm sorry, please check out our motivational quotes or some gifs to make you laugh");
};

function neutral() {
  alert("You could use a little laugh, check out some gifs");
};

function happy(){
  alert("Great, make sure to make someone else smile today");
};

var howOften = 5; //number often in seconds to rotate
var current = 0; //start the counter at 0
var ns6 = document.getElementById&&!document.all; //detect netscape 6

// place your images, text, etc in the array elements here
var items = new Array();
    items[0]="<img class='slideshow' alt='Motivationization' src='/images/fun.jpg' height='600' width='1000' border='0' />"; //a linked image
    items[1]="<img class='slideshow' alt='Motivationization' src='/images/balloonPic.jpg' height='600' width='1000' border='0' />"; //a linked image
    items[2]="<img class='slideshow' alt='Motivationization' src='/images/fun3.jpg' height='600' width='1000' border='0' />"; //a linked image
    items[3]="<img class='slideshow' alt='Motivationization' src='/images/fun4.jpg' height='600' width='1000' border='0' />"; //a linked image
function rotater() {
    document.getElementById("placeholder").innerHTML = items[current];
    current = (current==items.length-1) ? 0 : current + 1;
    setTimeout("rotater()",howOften*1000);
}

function rotater() {
    if(document.layers) {
        document.placeholderlayer.document.write(items[current]);
        document.placeholderlayer.document.close();
    }
    if(ns6)document.getElementById("placeholderdiv").innerHTML=items[current]
        if(document.all)
            placeholderdiv.innerHTML=items[current];

    current = (current==items.length-1) ? 0 : current + 1; //increment or reset
    setTimeout("rotater()",howOften*1000);
}
window.onload=rotater;
//-->
