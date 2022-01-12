// for search
document.querySelector("#search-icon").onclick = () => {
  document.querySelector("#search-form").classList.toggle("active");
};

document.querySelector("#close").onclick = () => {
  document.querySelector("#search-form").classList.remove("active");
};


const searchForm = document.querySelector("form");

// const searchResultDiv = document.querySelector(".search-result");
// const container = document.querySelector(".container");
let searchQuery = "";
const APP_ID = "2eb7968d";
const APP_key = "629ba1f4fb6403c68c9f783ca5228c61";
var from = 0;
var to = 5;

// const searchForm = document.querySelector("#search-form");
console.log(searchForm);
// searchForm.addEventListener("submit", (e) => {
//   e.preventDefault();
//   searchQuery = e.target.querySelector("input").value;
//   console.log(searchQuery);
//   fetchAPI();
// });

// async function fetchAPI() {
//   const spinner = document.querySelector(".spinner");
//   spinner.style.display = "block";
//   console.log("came here on fetchAPI");
//   const response = await fetch(`https://api.edamam.com/search?q=${searchQuery}&app_id=${APP_ID}&app_key=${APP_key}&from=${from}&to=${to}`);
//   const data = await response.json();
//   console.log(data);
// }











//   for menu bar
menuBar = () => {
  var x = document.querySelector("#navbar2");
  // console.log(x);
  // console.log("came here");
  if (x.style.display === "flex") {
    x.style.display = "none";
  } else {
    x.style.display = "flex";
  }
};


// to enabel dark theme
var dark = document.getElementById('dark');
dark.onclick = function (x) {
  document.body.classList.toggle("dark-theme");
}


//  preloader 
$(document).ready(function() {
  // console.log("preloder");
  preloaderFadeOutTime = 500;
  function hidePreloader() {
  var preloader = $('.spinner-wrapper');
  preloader.fadeOut(preloaderFadeOutTime);
  }
  hidePreloader();
  });


  //Add to cart option


function updateUserOrder(productId,action,username){
    // console.log("user is logged in ")
    var url = '/updatecart'
  
    fetch(url,{
      method:'POST',
      headers:{
        'Content-Type':'application/json',
        'X-CSRFToken':csrftoken,
      },
      body:JSON.stringify({'productId':productId, 'action':action, 'username':username})
      
  })
  .then((response)=>{
    return response.json()
  })
  .then((data)=>{
    console.log("updated");
  })
  .catch((error)=>{
    console.log(error)
  })
}


  var updateBtns = document.getElementsByClassName('update-cart')
  for (var i=0;i<updateBtns.length;i++){
    updateBtns[i].addEventListener('click',function(){
      var productId = this.dataset.product
      var action = this.dataset.action
      var username = this.dataset.username
      console.log(productId,action,username)
    
updateUserOrder(productId,action,username)

    })
  }

// error:-
// menu do not go away on resizeing the screen 
// window on resize will relode the page
// adding search fucntinality using ap id and key
