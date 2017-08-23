// Script to check if the (desired)cookie exist or not
// if it does then modify things according to it.

// Get all the cookies
var allcookies = document.cookie;
// Split all the cookies with  ';'
cookiearray = allcookies.split(';');

// Run through all the cookies
for(var i=0; i<cookiearray.length; i++) {
    name = cookiearray[i].split('=')[0];
    value = cookiearray[i].split('=')[1];
    // if a cookie with name 'user-trade' is found then execute if block
    if (name === 'user-trade') {
        // to modify the content of anchor tag if the div exists
        if(document.getElementById('user-register')) {
            var registerItem = document.getElementById('user-register');
            registerItem.href = "/dashboard/";
            registerItem.innerHTML = "Dashboard";
        }
        if(document.getElementById('user-login')) {
            var loginItem = document.getElementById('user-login');
            loginItem.href = '/logout/';
            loginItem.innerHTML = 'Logout';
        }
    }
}

// To not show login in nav bar if we are on login page
if((window.location.href).includes("login"))
    document.getElementById('user-login').style.display="none";

// To not show register in nav bar if we are on sign-up page
if((window.location.href).includes("signup"))
    document.getElementById('user-register').style.display="none";