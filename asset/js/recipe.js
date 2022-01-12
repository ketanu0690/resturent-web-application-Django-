const searchForm = document.querySelector("form");
const searchResultDiv = document.querySelector(".search-result");
const container = document.querySelector(".container");
let searchQuery = "";
const APP_ID = "2eb7968d";
const APP_key = "629ba1f4fb6403c68c9f783ca5228c61";
var from = 0;
var to = 5;

const next = () => {
  if (searchQuery == "") {
    alert("Please enter a search query");
  } else {
    if (to < 100) {
      const previous = document.querySelector(".previous");
      previous.style.display = "block";
        from += 5;
        to += 5;
        fetchAPI();
    }
  }
}

const previous = () => {

  if (searchQuery == "") {
    alert("Please enter a search query");
  } else { 
    
    if (from==1) {
      const previous = document.querySelector(".previous");
      previous.style.display = "none";
    }
    else {
      from -=5;
      to -=5;
      fetchAPI();
    }
  }
  }


searchForm.addEventListener("submit", (e) => {
  console.log("came here on submit");
  e.preventDefault();
  searchQuery = e.target.querySelector("input").value;
  console.log(searchQuery);
  fetchAPI();
});

async function fetchAPI() {
  const spinner = document.querySelector(".spinner");
  spinner.style.display = "block";
  console.log("came here on fetchAPI");
  const response = await fetch(`https://api.edamam.com/search?q=${searchQuery}&app_id=${APP_ID}&app_key=${APP_key}&from=${from}&to=${to}`);
  const data = await response.json();
  const loading = await(document.querySelector(".spinner").style.display = "none");
  spinner.style.display = "none";
  console.log(data);
  generateHTML(data.hits);
}

function generateHTML(results) {
  container.classList.remove("initial");
  let generatedHTML = "";
  results.map((result) => {
    generatedHTML += `
      <div class="item">
        <img src="${result.recipe.image}" alt="img">
        <div class="flex-container">
          <h1 class="title">${result.recipe.label}</h1>
          <a class="view-btn" target="_blank" href="${
            result.recipe.url
          }">View Recipe</a>
        </div>
        <p class="item-data">Calories: ${result.recipe.calories.toFixed(2)}</p>
        <p class="item-data">Diet label: ${
          result.recipe.dietLabels.length > 0
            ? result.recipe.dietLabels
            : "No Data Found"
        }</p>
        <p class="item-data">Health labels: ${result.recipe.healthLabels}</p>
      </div>
    `;
  });
  searchResultDiv.innerHTML = generatedHTML;
}


