const downArrow = document.querySelector('.down-arrow');
const heroImage = document.querySelector('.hero-image');
const heroHeading = document.querySelector('.hero-heading');
const ctaButtonHome = document.querySelector('.cta-btn-home');

window.onload = () => {
    if (downArrow) {
        downArrow.classList.add('animate__animated', 'animate__fadeInDown', 'animate__slower', 'animate__delay-3s');
    }
    if (heroImage) {
        heroImage.classList.add('animate__animated', 'animate__backInDown', 'animate__duration-1s');
    }
    if (heroHeading) {
        heroHeading.classList.add('animate__animated', 'animate__fadeIn', 'animate__slow', 'animate__delay-2s');
    }
    if (ctaButtonHome) {
        ctaButtonHome.classList.add('animate__animated', 'animate__fadeInLeft', 'animate__slow', 'animate__delay-3s');
    }
};
