const downArrow = document.querySelector('.down-arrow');
const heroHeading = document.querySelector('.hero-heading');
const ctaButtonHome = document.querySelector('.cta-btn-home');

window.onload = () => {
    if (downArrow) {
        downArrow.classList.remove('hide');
        downArrow.classList.add('animate__animated', 'animate__fadeInDown', 'animate__slower', 'animate__delay-1s');
    }
    if (heroHeading) {
        heroHeading.classList.remove('hide');
        heroHeading.classList.add('animate__animated', 'animate__fadeIn', 'animate__slow', 'animate__delay-1s');
    }
    if (ctaButtonHome) {
        ctaButtonHome.classList.remove('hide');
        ctaButtonHome.classList.add('animate__animated', 'animate__fadeInLeft', 'animate__slow', 'animate__delay-1s');
    }
};
