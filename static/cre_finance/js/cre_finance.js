let costForm = document.querySelectorAll(".cost-form");
let container = document.querySelector("#form-container");
let addButton = document.querySelector("#add-form");
let totalForms = document.querySelector("#id_form-TOTAL_FORMS");
let formNum = costForm.length-1;

function addForm(e) {
        e.preventDefault()

        let newForm = costForm[0].cloneNode(true)
        let formRegex = RegExp(`form-(\\d){1}-`,'g') //Regex to find all instances of the form number

        formNum++
        newForm.innerHTML = newForm.innerHTML.replace(formRegex, `form-${formNum}-`) //Update the new form to have the correct form number
        container.insertBefore(newForm, addButton) //Insert the new form at the end of the list of forms

        totalForms.setAttribute('value', `${formNum+1}`) //Increment the number of total forms in the management form
};

if (addButton) {
  addButton.addEventListener('click', addForm);
};

// leaflet https://leafletjs.com/examples/quick-start/


const lon = JSON.parse(document.getElementById('lon').textContent);
const lat = JSON.parse(document.getElementById('lat').textContent);
const name = JSON.parse(document.getElementById('name').textContent);

var map = L.map('map').setView([lat, lon], 13);

var mapBoxAccessToken = 'pk.eyJ1IjoiYmVhbmJlbiIsImEiOiJja3pyZmJqOTIwazd5MndtdTkzODFjcWwzIn0.6lG5lq6MiNZ4TRY7hwXDXA'

L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}', {
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
    maxZoom: 18,
    id: 'mapbox/streets-v11',
    tileSize: 512,
    zoomOffset: -1,
    accessToken: mapBoxAccessToken
}).addTo(map);


var marker = L.marker([lat, lon]).addTo(map);
marker.bindPopup("<b>" + name +"</b>").openPopup();
