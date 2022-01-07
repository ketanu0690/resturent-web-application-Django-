// for search
document.querySelector("#search-icon").onclick = () => {
  document.querySelector("#search-form").classList.toggle("active");
};

document.querySelector("#close").onclick = () => {
  document.querySelector("#search-form").classList.remove("active");
};

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
    
    console.log('data',data)
  })
  
  }

  var updateBtns = document.getElementsByClassName('update-cart')
  for (var i=0;i<updateBtns.length;i++){
    updateBtns[i].addEventListener('click',function(){
      var productId = this.dataset.product
      var action = this.dataset.action
      var username = this.dataset.username
      // console.log("username here",username)
      // console.log('ProductId',productId,'action',action,'username',username)
updateUserOrder(productId,action,username)

    })
  }




  // console.log("cart added");

// error:-
// menu do not go away on resizeing the screen 
// window on resize will relode the page

  