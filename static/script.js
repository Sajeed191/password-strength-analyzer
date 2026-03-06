function togglePassword(){

let pass = document.getElementById("password");

if(pass.type === "password")
pass.type = "text";
else
pass.type = "password";

}


function checkPassword(){

let password = document.getElementById("password").value;
let website = document.getElementById("website").value;

fetch("/analyze",{

method:"POST",

headers:{
"Content-Type":"application/json"
},

body:JSON.stringify({
password:password,
website:website
})

})

.then(res=>res.json())
.then(data=>{

document.getElementById("strengthText").innerText =
"Strength : " + data.strength;

document.getElementById("bar").style.width =
data.percent + "%";

document.getElementById("similarity").innerText =
data.similarity + "% users used similar passwords on " + website;

let list = document.getElementById("suggestions");

list.innerHTML="";

data.suggestions.forEach(p=>{

let li = document.createElement("li");

li.innerText=p;

list.appendChild(li);

});

});

}