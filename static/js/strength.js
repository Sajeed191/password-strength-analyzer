let password = document.getElementById("password")
let bar = document.getElementById("strength-bar")
let text = document.getElementById("strength-text")

password.addEventListener("input", function(){

let value = password.value

let score = 0

if(value.length >= 8){
score++
}

if(/[A-Z]/.test(value)){
score++
}

if(/[0-9]/.test(value)){
score++
}

if(/[@$!%*?&]/.test(value)){
score++
}

if(score == 1){
bar.style.width = "25%"
bar.style.background = "red"
text.innerText = "Weak"
}

else if(score == 2){
bar.style.width = "50%"
bar.style.background = "orange"
text.innerText = "Medium"
}

else if(score == 3){
bar.style.width = "75%"
bar.style.background = "yellow"
text.innerText = "Strong"
}

else if(score == 4){
bar.style.width = "100%"
bar.style.background = "green"
text.innerText = "Very Strong"
}

else{
bar.style.width = "0%"
text.innerText = ""
}

})
