const calendarButton = document.querySelector('#calendarButton');

calendarButton?.addEventListener('click', () => {
  const calendar = [
    'BEGIN:VCALENDAR',
    'VERSION:2.0',
    'PRODID:-//Haolin Baptism//Invitation//EN',
    'BEGIN:VEVENT',
    'UID:haolin-baptism-20260726@example.local',
    'DTSTAMP:20260701T120000Z',
    'DTSTART:20260726T230000Z',
    'DTEND:20260727T003000Z',
    'SUMMARY:Haolin Luo’s Baptism',
    'DESCRIPTION:Join us to celebrate Haolin Luo’s baptism.',
    'END:VEVENT',
    'END:VCALENDAR'
  ].join('\r\n');

  const blob = new Blob([calendar], { type: 'text/calendar;charset=utf-8' });
  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.download = 'haolin-luo-baptism.ics';
  link.click();
  URL.revokeObjectURL(url);
});

const lightbox = document.querySelector('#lightbox');
const lightboxImage = lightbox?.querySelector('img');
const closeButton = lightbox?.querySelector('.lightbox-close');

document.querySelectorAll('.photo').forEach((photo) => {
  photo.addEventListener('click', () => {
    lightboxImage.src = photo.dataset.src;
    lightboxImage.alt = photo.dataset.alt;
    lightbox.showModal();
  });
});

closeButton?.addEventListener('click', () => lightbox.close());
lightbox?.addEventListener('click', (event) => {
  if (event.target === lightbox) lightbox.close();
});

const slideshow = document.querySelector('.photo-slideshow');
const slides = [...document.querySelectorAll('.photo-slideshow .photo')];
const previousButton = document.querySelector('.slideshow-prev');
const nextButton = document.querySelector('.slideshow-next');
const slideshowStatus = document.querySelector('.slideshow-status span');
const dotsContainer = document.querySelector('.slideshow-dots');
let currentSlide = 0;
let slideshowTimer;

const dots = slides.map((_, index) => {
  const dot = document.createElement('button');
  dot.className = `slideshow-dot${index === 0 ? ' active' : ''}`;
  dot.type = 'button';
  dot.setAttribute('aria-label', `Show photo ${index + 1}`);
  dot.addEventListener('click', () => {
    showSlide(index);
    restartSlideshow();
  });
  dotsContainer?.append(dot);
  return dot;
});

function showSlide(index) {
  currentSlide = (index + slides.length) % slides.length;
  slides.forEach((slide, slideIndex) => {
    const active = slideIndex === currentSlide;
    slide.classList.toggle('active', active);
    slide.setAttribute('aria-hidden', String(!active));
    slide.tabIndex = active ? 0 : -1;
  });
  dots.forEach((dot, dotIndex) => dot.classList.toggle('active', dotIndex === currentSlide));
  if (slideshowStatus) slideshowStatus.textContent = String(currentSlide + 1);
}

function startSlideshow() {
  clearInterval(slideshowTimer);
  slideshowTimer = setInterval(() => showSlide(currentSlide + 1), 5000);
}

function restartSlideshow() {
  startSlideshow();
}

previousButton?.addEventListener('click', () => {
  showSlide(currentSlide - 1);
  restartSlideshow();
});

nextButton?.addEventListener('click', () => {
  showSlide(currentSlide + 1);
  restartSlideshow();
});

slideshow?.addEventListener('keydown', (event) => {
  if (event.key === 'ArrowLeft') previousButton?.click();
  if (event.key === 'ArrowRight') nextButton?.click();
});

slideshow?.addEventListener('mouseenter', () => clearInterval(slideshowTimer));
slideshow?.addEventListener('mouseleave', startSlideshow);
slideshow?.addEventListener('focusin', () => clearInterval(slideshowTimer));
slideshow?.addEventListener('focusout', (event) => {
  if (!slideshow.contains(event.relatedTarget)) startSlideshow();
});
document.addEventListener('visibilitychange', () => {
  if (document.hidden) clearInterval(slideshowTimer);
  else startSlideshow();
});

showSlide(0);
startSlideshow();
