document.addEventListener("DOMContentLoaded", function () {
  // Smooth scrolling for navigation links remains unchanged.
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

  // Initialize all slideshow containers independently.
  const slideshows = document.querySelectorAll('.slideshow-container');
  slideshows.forEach(container => {
    // Set initial index for each container
    container.dataset.slideIndex = 1;
    const slides = container.querySelectorAll('.mySlides');
    // Hide all slides initially.
    slides.forEach(slide => {
      slide.style.display = "none";
      slide.style.opacity = 0;
    });
    // Show the first slide.
    showSlides(container, 1);
    // Start auto-loop for this slideshow
    setInterval(() => {
      plusSlides(container, 1);
    }, 10000);
  });

  // Attach click events to arrow controls for each container.
  document.querySelectorAll('.prev').forEach(prevArrow => {
    prevArrow.addEventListener('click', function () {
      const container = this.closest('.slideshow-container');
      plusSlides(container, -1);
    });
  });

  document.querySelectorAll('.next').forEach(nextArrow => {
    nextArrow.addEventListener('click', function () {
      const container = this.closest('.slideshow-container');
      plusSlides(container, 1);
    });
  });
});

// Fade in: Increase opacity from 0 to 1 over the given duration (milliseconds)
function fadeIn(element, duration, callback) {
  element.style.opacity = 0;
  element.style.display = "block";
  let startTime = null;
  function animateFadeIn(timestamp) {
    if (!startTime) startTime = timestamp;
    let elapsed = timestamp - startTime;
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

// Fade out: Decrease opacity from 1 to 0 over the given duration (milliseconds)
function fadeOut(element, duration, callback) {
  element.style.opacity = 1;
  let startTime = null;
  function animateFadeOut(timestamp) {
    if (!startTime) startTime = timestamp;
    let elapsed = timestamp - startTime;
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

// Main function to show the desired slide for a given slideshow container with fade transitions
function showSlides(container, n) {
  const slides = container.querySelectorAll('.mySlides');
  // If you have dot navigation for each container, update this selection:
  const dots = container.querySelectorAll('.dot');
  
  let slideIndex = parseInt(container.dataset.slideIndex) || 1;
  if (n > slides.length) {
    slideIndex = 1;
  } else if (n < 1) {
    slideIndex = slides.length;
  } else {
    slideIndex = n;
  }
  container.dataset.slideIndex = slideIndex;

  // Update dot navigation if present.
  if (dots.length) {
    dots.forEach(dot => dot.classList.remove("active"));
    if (dots[slideIndex - 1]) {
      dots[slideIndex - 1].classList.add("active");
    }
  }

  const targetSlide = slides[slideIndex - 1];

  // Identify the currently visible slide, if any.
  let currentSlide = null;
  slides.forEach(slide => {
    if (slide.style.display === "block") {
      currentSlide = slide;
    }
  });

  // Fade transitions: if a different slide is visible, fade it out then fade in the target slide.
  if (currentSlide && currentSlide !== targetSlide) {
    fadeOut(currentSlide, 1000, function () {
      fadeIn(targetSlide, 3000);
    });
  } else {
    fadeIn(targetSlide, 3000);
  }
}

// Navigation controls: move to the next or previous slide for the given container.
function plusSlides(container, n) {
  let currentIndex = parseInt(container.dataset.slideIndex) || 1;
  showSlides(container, currentIndex + n);
}
