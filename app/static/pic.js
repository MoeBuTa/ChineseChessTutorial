
var imgList = document.getElementById("img-list");

var imgArr = document.getElementsByTagName("img");

imgList.style.width = 475 * imgArr.length + "px";

var btn = document.getElementById("btn");

var imgBox = document.getElementById("img-box");

btn.style.left = (imgBox.offsetWidth - btn.offsetWidth)/2 + "px";

var index = 0;

var allA = document.getElementsByClassName("imageA");

allA[index].style.backgroundColor = "#ff6700";

for(var i = 0; i < allA.length; i++){
    allA[i].number = i;

    allA[i].onclick = function(){
        clearInterval(time);
        index = this.number;
        imgList.style.left = -475 * index + "px";
        setA();
        auto();
    };
}

auto();

function setA(){
    if(index >= imgArr.length -1){
        index = 0;
        imgList.style.left = 0;
    }

    for(var i = 0; i < allA.length; i++){
        allA[i].style.backgroundColor = "";
    }
    allA[index].style.backgroundColor = "#ff6700";
}

var time;

function auto(){
    time = setInterval(function(){
        index++;
        index %= imgArr.length;
        imgList.style.left = -475 * index + "px";
        setA();
    },3000);
}
