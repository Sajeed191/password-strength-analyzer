function checkStrength(){

let password = document.getElementById("password").value
let strength = document.getElementById("strength")

let score = 0

if(password.length > 8) score++
if(/[A-Z]/.test(password)) score++
if(/[0-9]/.test(password)) score++
if(/[!@#$%^&*]/.test(password)) score++

if(score <=1){
strength.innerHTML="Weak"
strength.style.color="red"
}

else if(score==2){
strength.innerHTML="Medium"
strength.style.color="orange"
}

else{
strength.innerHTML="Strong"
strength.style.color="lime"
}

}
