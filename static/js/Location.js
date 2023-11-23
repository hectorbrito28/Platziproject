function getLocation() {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition((position) => {
      const coords = position.coords;
      alert(`Tu latitud es: ${coords.latitude}, Tu longitud es longitud: ${coords.longitude}`);
    });
  } else {
    $demo.text("Geolocation is not supported by this browser.");
  }
}


