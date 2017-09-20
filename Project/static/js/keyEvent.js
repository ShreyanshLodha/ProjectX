function myKeyPress(e){
var x = event.charCode || e.keyCode;   // Get the Unicode value
var y = String.fromCharCode(x);          // Convert the value into a character
if (y==='['){
    // Buy module call
    alert("Buy");
}
else if(y===']'){
    // Sell module call.
    alert("Sell");
}
}