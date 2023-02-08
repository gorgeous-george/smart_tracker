<!-- JS to hide flash message after 3 sec timeout -->
var message_ele = document.getElementById("message_container");

// Timeout is 3 sec
setTimeout(function(){
   message_ele.style.display = "none";
}, 3000);