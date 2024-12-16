const sign_in_btn = document.querySelector("#sign-in-btn");
const sign_up_btn = document.querySelector("#sign-up-btn");
const container = document.querySelector(".container");

// Toggle between Sign Up and Sign In modes
sign_up_btn.addEventListener("click", () => {
  container.classList.add("sign-up-mode");
});

sign_in_btn.addEventListener("click", () => {
  container.classList.remove("sign-up-mode");
});


var allValue = [
  'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
  'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '1', '2', '3', '4', '5', 
  '6', '7', '8', '9', '0'
];

function generateCaptcha() {
  let cValue = "";
  for (let i = 0; i < 6; i++) {
    cValue += allValue[Math.floor(Math.random() * allValue.length)];
  }
  return cValue;
}

// Set initial captchas
const captchaValueSignIn = document.querySelector("#captchaValueSignIn");
const captchaValueSignUp = document.querySelector("#captchaValueSignUp");

const inputCaptchaSignIn = document.querySelector("#inputCaptchaSignIn");
const inputCaptchaSignUp = document.querySelector("#inputCaptchaSignUp");

const submitBtnSignIn = document.querySelector("#submitBtnSignIn");
const submitBtnSignUp = document.querySelector("#submitBtnSignUp");

let currentCaptchaSignIn = generateCaptcha();
let currentCaptchaSignUp = generateCaptcha();

captchaValueSignIn.textContent = currentCaptchaSignIn;
captchaValueSignUp.textContent = currentCaptchaSignUp;

// Validate Sign In captcha
submitBtnSignIn.addEventListener("click", () => {
  const inputValue = inputCaptchaSignIn.value;
  if (inputValue === currentCaptchaSignIn) {
    alert("Sign In Successful");
    // Add your form submission logic here
    document.querySelector("#signInForm").submit();
  } else if (inputValue === "") {
    alert("Invalid Captcha: Field is Empty");
  } else {
    alert("Invalid Captcha: Try Again");
  }
});


submitBtnSignUp.addEventListener("click", () => {
  const inputValue = inputCaptchaSignUp.value;
  if (inputValue === currentCaptchaSignUp) {
    alert("Sign Up Successful");
 
    document.querySelector("#signUpForm").submit();
  } else if (inputValue === "") {
    alert("Invalid Captcha: Field is Empty");
  } else {
    alert("Invalid Captcha: Try Again");
  }
});
