const para=document.getElementById('timer')
var difference=document.getElementById('time_left').value
topicId=document.getElementById('topicId').value

const url=window.location.origin

var x = setInterval(function(){

    var minutes=Math.floor(difference/60)
    var seconds=Math.floor(difference%60)

    if(minutes<10){
        minutes="0"+minutes
    }
    if(seconds<10){
        seconds="0"+seconds
    }

    if(minutes<1 && seconds<60){
        para.style.color="red";
    }
    time_left=minutes +":"+ seconds

    difference--

    if (difference < 0) {
        clearInterval(x);
        time_left="Times Up!"
        window.location.href= url+ "/score/" + topicId
      }
      document.getElementById('timer').innerHTML = time_left
}, 1000);

function preventBack() {
    window.history.forward();
}
setTimeout("preventBack()", 0);  
window.onunload = function () { null };

if ( window.history.replaceState ) {
    window.history.replaceState( null, null, window.location.href );
}