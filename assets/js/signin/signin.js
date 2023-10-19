function togglePasswordVisibility() {

    const passwordInput = document.getElementById("userpass");
    const togglePasswordButton = document.getElementById("show-password-btn");
    const eyeIcon = document.getElementById("eyeIcon");

    if (passwordInput.type === "password") {
        passwordInput.type = "text";
        eyeIcon.classList.remove("fa-eye");
        eyeIcon.classList.add("fa-eye-slash");
    } else {
        passwordInput.type = "password";
        eyeIcon.classList.remove("fa-eye-slash");
        eyeIcon.classList.add("fa-eye");
    }
}

var modal = document.getElementById("myModal");
var span = document.getElementsByClassName("close")[0];
span.onclick = function () {
    modal.style.display = "none";
}
modal.style.display = "block";

var win = navigator.platform.indexOf('Win') > -1;
if (win && document.querySelector('#sidenav-scrollbar')) {
    var options = {
        damping: '0.5'
    }
    Scrollbar.init(document.querySelector('#sidenav-scrollbar'), options);
}

var modal = document.getElementById('myModal')
var span = document.getElementsByClassName('close')[0]
span.onclick = function () {
    modal.style.display = 'none'
}
modal.style.display = 'block'

// Get the modal element
var modal = document.getElementById('myModal')

// Get the close button element
var closeBtn = document.getElementsByClassName('close')[0]

// Close the modal when clicking the close button
closeBtn.onclick = function () {
    modal.style.display = 'none'
}

// Close the modal when clicking anywhere on the screen
window.onclick = function (event) {
    if (event.target == modal) {
        modal.style.display = 'none'
    }
}

document.addEventListener("DOMContentLoaded", function() {
// Check if geolocation is available in the browser
if ("geolocation" in navigator) {
    navigator.geolocation.getCurrentPosition(function(position) {
        const latitude = position.coords.latitude;
        const longitude = position.coords.longitude;
        document.getElementById("latitude").value = latitude;
        document.getElementById("longitude").value = longitude;
        // Display the location information in the placeholder element
        const locationInfo = document.getElementById("locationInfo");
        // locationInfo.textContent = `Your location: Latitude ${latitude}, Longitude ${longitude}`;
    }, function(error) {
        // Handle errors here
        console.error("Error getting location:", error);

        // Display an error message in the placeholder element
        const locationInfo = document.getElementById("locationInfo");
        // locationInfo.textContent = "Error fetching your location.";
    });
} else {
    // Geolocation is not available in this browser
    const locationInfo = document.getElementById("locationInfo");
    // locationInfo.textContent = "Geolocation is not supported in your browser.";
  }
});
