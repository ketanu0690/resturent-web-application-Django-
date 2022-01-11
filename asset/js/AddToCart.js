console.log("AddToCart.js");


function updateUserOrder(productId,action,username){

    var url = '/updatecart'
  
    fetch(url,{
      method:'POST',
      headers:{
        'Content-Type':'application/json',
        'X-CSRFToken':csrftoken,
      },
      body:JSON.stringify({'productId':productId, 'action':action, 'username':username })
  })
  .then((response)=>{

    return response.json()
  })
  .then((data)=>{
  })
  .catch((error)=>{
  })
}


var updateBtns = document.getElementsByClassName('update-cart')
  for (var i=0;i<updateBtns.length;i++){
    updateBtns[i].addEventListener('click',function(){
      var productId = this.dataset.product
      var action = this.dataset.action
      var username = this.dataset.username
      console.log(productId,action,username);
      
     
updateUserOrder(productId,action,username)


})
}