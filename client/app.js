function getBathValue() {
  var uiBathrooms = document.getElementsByName("uiBathrooms");
  for (var i = 0; i < uiBathrooms.length; i++) {
    if (uiBathrooms[i].checked) {
      return i + 1;
    }
  }
  return -1; // Invalid Value
}

function getBHKValue() {
  var uiBHK = document.getElementsByName("uiBHK");
  for (var i = 0; i < uiBHK.length; i++) {
    if (uiBHK[i].checked) {
      return i + 1;
    }
  }
  return -1; // Invalid Value
}

function getFloorValue() {
  var uiFloors = document.getElementsByName("uiFloors");
  for (var i = 0; i < uiFloors.length; i++) {
    if (uiFloors[i].checked) {
      return i + 1;
    }
  }
  return -1; // Invalid Value
}

function onClickedEstimatePrice() {
  console.log("Estimate price button clicked");
  var sqft = document.getElementById("uiSqft").value;
  var bhk = getBHKValue();
  var bathrooms = getBathValue();
  var floor = getFloorValue();
  var location = document.getElementById("uiLocations").value;
  var estPrice = document.getElementById("uiEstimatedPrice");

  var url = "https://house-price-prediction-self.vercel.app/api/predict_home_price";
  // Update this with your actual Vercel deployment URL

  fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      sqft: parseFloat(sqft),
      bhk: bhk,
      bath: bathrooms,
      floor: floor,
      location: location,
    }),
  })
    .then((response) => response.json())
    .then((data) => {
      console.log(data.estimated_price);
      estPrice.innerHTML =
        "<h2>" + data.estimated_price.toString() + " Rupees</h2>";
    })
    .catch((error) => {
      console.error("Error occurred:", error);
      estPrice.innerHTML =
        "<h2>Unable to estimate price. Please try again.</h2>";
    });
}

function onPageLoad() {
  console.log("document loaded");
  var url = "https://house-price-prediction-self.vercel.app/api/get_location_names";
 // Update this with your actual Vercel deployment URL

  fetch(url)
    .then((response) => response.json())
    .then((data) => {
      console.log("got response for get_location_names request");
      if (data) {
        var locations = data.locations;
        var uiLocations = document.getElementById("uiLocations");
        uiLocations.innerHTML = ""; // Clear existing options
        locations.forEach((loc) => {
          var opt = new Option(loc);
          uiLocations.appendChild(opt);
        });
      }
    })
    .catch((error) => console.error("Error fetching locations:", error));
}

window.onload = onPageLoad;
