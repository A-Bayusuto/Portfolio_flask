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

let slideIndex = 1;

// Fade-in: Increase opacity from 0 to 1 over the given duration (milliseconds)
function fadeIn(element, duration, callback) {
  element.style.opacity = 0;
  element.style.display = "block";
  let startTime = null;
  function animateFadeIn(timestamp) {
    if (!startTime) startTime = timestamp;
    let elapsed = timestamp - startTime;
    // Calculate new opacity, ensuring it does not exceed 1
    let newOpacity = Math.min(elapsed / duration, 1);
    element.style.opacity = newOpacity;
    if (elapsed < duration) {
      requestAnimationFrame(animateFadeIn);
    } else {
      element.style.opacity = 1;
      if (callback) callback();
    }
  }
  requestAnimationFrame(animateFadeIn);
}

// Fade-out: Decrease opacity from 1 to 0 over the given duration (milliseconds)
function fadeOut(element, duration, callback) {
  element.style.opacity = 1;
  let startTime = null;
  function animateFadeOut(timestamp) {
    if (!startTime) startTime = timestamp;
    let elapsed = timestamp - startTime;
    // Calculate new opacity, ensuring it does not drop below 0
    let newOpacity = Math.max(1 - elapsed / duration, 0);
    element.style.opacity = newOpacity;
    if (elapsed < duration) {
      requestAnimationFrame(animateFadeOut);
    } else {
      element.style.opacity = 0;
      element.style.display = "none";
      if (callback) callback();
    }
  }
  requestAnimationFrame(animateFadeOut);
}

// Main function to show the desired slide with fade transitions and update the dot navigation
function showSlides(n) {
  const slides = document.getElementsByClassName("mySlides");
  const dots = document.getElementsByClassName("dot");

  // Wrap the slide index if it overflows or underflows
  if (n > slides.length) {
    slideIndex = 1;
  } else if (n < 1) {
    slideIndex = slides.length;
  }
  const targetIndex = slideIndex - 1;

  // Update dot navigation: remove "active" from all and add it to the current one
  Array.from(dots).forEach(dot => (dot.className = dot.className.replace(" active", "")));
  if (dots[targetIndex]) {
    dots[targetIndex].className += " active";
  }

  // Find the currently visible slide
  let currentSlide = null;
  for (let i = 0; i < slides.length; i++) {
    if (slides[i].style.display === "block") {
      currentSlide = slides[i];
      break;
    }
  }
  const targetSlide = slides[targetIndex];

  // If a different slide is visible, fade it out first before fading in the target slide
  if (currentSlide && currentSlide !== targetSlide) {
    fadeOut(currentSlide, 1000, function() {
      fadeIn(targetSlide, 3000);
    });
  } else {
    fadeIn(targetSlide, 3000);
  }
}

// Navigation controls
function plusSlides(n) {
  showSlides(slideIndex += n);
}

function currentSlide(n) {
  showSlides(slideIndex = n);
}

// Auto-loop: Move to the next slide every 5 seconds
function autoLoopSlides() {
  setInterval(() => {
    plusSlides(1);
  }, 10000);
}

// On window load, hide all slides, show the first slide, and start auto-looping
window.onload = function() {
  const slides = document.getElementsByClassName("mySlides");
  for (let i = 0; i < slides.length; i++) {
    slides[i].style.display = "none";
    slides[i].style.opacity = 0;
  }
  showSlides(slideIndex);
  autoLoopSlides();
};
