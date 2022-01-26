// for search
document.querySelector("#search-icon").onclick = () => {
  document.querySelector("#search-form").classList.toggle("active");
};

document.querySelector("#close").onclick = () => {
  document.querySelector("#search-form").classList.remove("active");
};

const searchForm = document.querySelector("form");
let searchQuery = "";
const APP_ID = "2eb7968d";
const APP_key = "629ba1f4fb6403c68c9f783ca5228c61";
var from = 0;
var to = 5;
// console.log(searchForm);

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
var dark = document.getElementById("dark");
dark.onclick = function (x) {
  document.body.classList.toggle("dark-theme");
};

//  preloader
$(document).ready(function () {
  // console.log("preloder");
  preloaderFadeOutTime = 500;
  function hidePreloader() {
    var preloader = $(".spinner-wrapper");
    preloader.fadeOut(preloaderFadeOutTime);
  }
  hidePreloader();
});

//Add to cart option
async function updateUserOrder(productId, action, username) {
  // console.log("user is logged in ")
  var url = "/updatecart";

 await fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrftoken,
    },
    body: JSON.stringify({
      productId: productId,
      action: action,
      username: username,
    }),
  })
    . then((response) => {
      return response.json();
    })
    .then((data) => {
      console.log("updated");
       window.location.reload()
    })
    .catch((error) => {
      console.log(error);
    });
}

var updateBtns = document.getElementsByClassName("update-cart");
for (var i = 0; i < updateBtns.length; i++) {
  updateBtns[i].addEventListener("click", function () {
    var productId = this.dataset.product;
    var action = this.dataset.action;
    var username = this.dataset.username;
    console.log(productId, action, username);

    updateUserOrder(productId, action, username);
  });
}

// for chat bot
var msg = "0";

document.querySelector("#chat-circle").onclick = (e) => {
  console.log("clicked");
  
  msg = {
    "msg" : "My name is stark. Let's have a conversation! Also, if you want to exit any time, just type Bye!"
  }
    
  generate_message(msg,"bot");

};

// $(function() {

var INDEX = 0;
$("#chat-submit").click(function (e) {
  e.preventDefault();

  var msg = $("#chat-input").val();

  if (msg.trim() == "") {
    console.log("empty");
    return false;
  }
  generate_message(msg,"user");
  // sending msg to python Function chatbot
  $.ajax({
    url: "/chatbot",
    type: "POST",
    data: {
      msg: msg,
      flag: "True",
      csrfmiddlewaretoken: csrftoken,
    },
    success: function (data) {
      // console.log("printing data from console here ", data);
      // console.log(data.msg);
      // console.log(data.flag);

      generate_message(data,"bot");
      $("#chat-input").val("");
      msg = data;
    },
    error: function (xhr, errmsg, err) {
      console.log(xhr.status + ": " + xhr.responseText);
    },
  });
});

function generate_message(msg, type) {
  // console.log("generate message");
  var str = "";
  INDEX++;
  if (type == "bot") {
    str += "<div id='cm-msg-" + INDEX + "' class=\"chat-msg " + type + '">';
    str += '          <div class="cm-msg-text">';
    
    str +="bot :"+ msg.msg;
    
    str += "          </div>";
    str += "        </div>";
    $(".chat-logs").append(str);
    $("#cm-msg-" + INDEX)
      .hide()
      .fadeIn(300);
      // console.log("bot");
  } else {
    
    str += "<div id='cm-msg-" + INDEX + "' class=\"chat-msg " + type + '">';
    str += '          <div class="cm-msg-text">';
    str +=  "user message "+msg;
    str += "          </div>";
    str += "        </div>";
    $(".chat-logs").append(str);
    $("#cm-msg-" + INDEX)
      .hide()
      .fadeIn(300);
  // console.log("user");
    }


  if (type == "self") {
    $("#chat-input").val("");
  }
  $(".chat-logs")
    .stop()
    .animate({ scrollTop: $(".chat-logs")[0].scrollHeight }, 1000);
}

$(document).delegate(".chat-btn", "click", function () {
  var value = $(this).attr("chat-value");
  var name = $(this).html();
  $("#chat-input").attr("disabled", false);
  generate_message(name, "self");
});

$("#chat-circle").click(function () {
  $("#chat-circle").toggle("scale");
  $(".chat-box").toggle("scale");
});

$(".chat-box-toggle").click(function () {
  $("#chat-circle").toggle("scale");
  $(".chat-box").toggle("scale");
});

// })

// error:-
// menu do not go away on resizeing the screen
// window on resize will relode the page
// adding search fucntinality using ap id and key
