
var button1 = document.getElementById("clickmeup"),
    count = 0;
    button1.onclick = function() {
        count += 1;
        document.getElementById("output").innerHTML = count;
    };


var button2 = document.getElementById("clickmedown"),
    count = 0;
    button2.onclick = function() {
        count -= 1;
        document.getElementById("output").innerHTML = count;
    };