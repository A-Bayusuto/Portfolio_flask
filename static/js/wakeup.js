// Wait for the DOM content to load before starting the jump scare logic
document.addEventListener("DOMContentLoaded", function() {
    // Set a delay (in milliseconds) before triggering the jump scare.
    // Change 3000 to a longer value (like 5000) if you'd like to delay further.
    setTimeout(triggerJumpScare, 3000);
  });
  
  function triggerJumpScare() {
    const jumpScare = document.getElementById("jumpScare");
    // Show the jump scare overlay immediately
    jumpScare.style.display = "block";
    
    // Play a scary sound; replace 'scarySound.mp3' with your actual sound file
    // const screamAudio = new Audio('scarySound.mp3');
    // screamAudio.play();
  
    // Optionally, remove the jump scare overlay after 5 seconds.
    // Adjust the delay as needed (5000 = 5 seconds)
    setTimeout(function() {
      jumpScare.style.display = "none";
    }, 5000);
  }
  