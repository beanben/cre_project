// < ===== leaflet https://leafletjs.com/examples/quick-start/
console.log("mapjs loaded");

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
