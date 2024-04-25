
document.addEventListener('DOMContentLoaded', function () {
    const carousel = document.querySelector('.carousel');
    const carouselInner = carousel.querySelector('.carousel-inner');
    const prevBtn = carousel.querySelector('.prev');
    const nextBtn = carousel.querySelector('.next');
  
    let currentIndex = 0;
    const totalSlides = carouselInner.children.length;
  
    prevBtn.addEventListener('click', function () {
      if (currentIndex > 0) {
        currentIndex--;
        updateCarousel();
      }
    });
  
    nextBtn.addEventListener('click', function () {
      if (currentIndex < totalSlides - 1) {
        currentIndex++;
        updateCarousel();
      }
    });
  
    function updateCarousel() {
      const slideWidth = carouselInner.clientWidth;
      const offset = -currentIndex * slideWidth;
      carouselInner.style.transform = `translateX(${offset}px)`;
    }
  });
  