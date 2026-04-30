// the map page

//the teacher data
const rawData = sessionStorage.getItem("userData");
const userData = rawData ? JSON.parse(rawData) : null;
const teacherId = userData ? userData.id : null;

if (!teacherId) {
  alert("Please log in first!");
  window.location.href = "/frontend/login.html";
}
//show the map (the view is Jerusalem)
var map = L.map("map").setView([31.7767, 35.2345], 16);

L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
  attribution: "© OpenStreetMap",
}).addTo(map);

async function loadStudentLocations() {
  try {
    const response = await fetch(`/latest_locations?teacher_id=${teacherId}`);
    const locations = await response.json();
    if (!locations || locations.length === 0) return;
    const teacher = locations[0];
    //before the changes we clear and then we put the new
    map.eachLayer((layer) => {
      if (layer instanceof L.Marker) {
        map.removeLayer(layer);
      }
    });

    locations.forEach((loc, index) => {
      if (loc.latitude && loc.longitude) {
        let popupContent = "";
        if (index === 0) {
          popupContent = `<b>You</b>`;
        } else {
          const distance = calculateAirDistance(
            teacher.latitude,
            teacher.longitude,
            loc.latitude,
            loc.longitude,
          );
          if (distance > 3) {
            popupContent = `<b style="color:red;">WARNING: Student ${loc.student_id} is far away!</b>`;
          } else {
            popupContent = `<b>Student ID:</b> ${loc.student_id}`;
          }
        }
        L.marker([loc.latitude, loc.longitude])
          .addTo(map)
          .bindPopup(popupContent);
      }
    });
  } catch (error) {
    console.error("Error loading locations:", error);
  }
}

// Calculate the air distance between two points using the Haversine formula
function calculateAirDistance(lat1, lon1, lat2, lon2) {
  const R = 6371; // Earth's radius in kilometers
  const dLat = (lat2 - lat1) * (Math.PI / 180);
  const dLon = (lon2 - lon1) * (Math.PI / 180);
  const a =
    Math.sin(dLat / 2) * Math.sin(dLat / 2) +
    Math.cos(lat1 * (Math.PI / 180)) *
      Math.cos(lat2 * (Math.PI / 180)) *
      Math.sin(dLon / 2) *
      Math.sin(dLon / 2);
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
  //return the distance in kilometers
  return R * c;
}
loadStudentLocations();
setInterval(loadStudentLocations, 30000);
