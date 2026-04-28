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
//before the changes we clear and then we put the new
      map.eachLayer((layer) => {
        if (layer instanceof L.Marker) {
          map.removeLayer(layer);
        }
      });

      locations.forEach((loc) => {
        if (loc.latitude && loc.longitude) {
          L.marker([loc.latitude, loc.longitude])
            .addTo(map)
            .bindPopup(`<b>Student ID:</b> ${loc.student_id}`);
        }
      });
    } catch (error) {
      console.error("Error loading locations:", error);
    }
  }

  loadStudentLocations();
  setInterval(loadStudentLocations, 30000);
