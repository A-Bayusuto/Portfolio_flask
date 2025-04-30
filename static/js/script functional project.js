document.addEventListener("DOMContentLoaded", function () {
    // Smooth scrolling for navigation links
    document.querySelectorAll(".sidebar a").forEach(anchor => {
      anchor.addEventListener("click", function (event) {
        event.preventDefault();
        const targetId = this.getAttribute("href").substring(1);
        const targetSection = document.getElementById(targetId);
        if (targetSection) {
          targetSection.scrollIntoView({ behavior: "smooth" });
        }
      });
    });
})

let slideIndex = 1; // Initial slide index

function initializeSlides() {
  let slides = document.getElementsByClassName("mySlides");
  
  // Set all slides to "display: none"
  for (let i = 0; i < slides.length; i++) {
      slides[i].style.display = "none";
  }

  // Display the first slide
  slides[slideIndex - 1].style.display = "block";
}

initializeSlides(); // Initialize styles for all slides

showSlides(slideIndex); // Display the first slide

// Next/previous controls
function plusSlides(n) {
    showSlides(slideIndex += n);
}

// Thumbnail dot controls (optional)
function currentSlide(n) {
    showSlides(slideIndex = n);
}

// Display the relevant slide
function showSlides(n) {
    let slides = document.getElementsByClassName("mySlides"); // Select all slides
    let dots = document.getElementsByClassName("dot"); // Select dots for navigation
    if (n > slides.length) { slideIndex = 1; } // Reset to the first slide if overflow
    if (n < 1) { slideIndex = slides.length; } // Reset to the last slide if underflow

    // Hide all slides and remove 'active' class from dots
    for (let i = 0; i < slides.length; i++) {
        slides[i].style.display = "none";
    }
    for (let i = 0; i < dots.length; i++) {
        dots[i].className = dots[i].className.replace(" active", "");
    }

    // Show the current slide and highlight the corresponding dot
    slides[slideIndex - 1].style.display = "block";
    dots[slideIndex - 1].className += " active";
}