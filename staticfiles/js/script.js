const downArrow = document.querySelector('.down-arrow');
const heroHeading = document.querySelector('.hero-heading');
const ctaButtonHome = document.querySelector('.cta-btn-home');

window.onload = () => {
    if (downArrow) {
        downArrow.classList.remove('hide');
        downArrow.classList.add('animate__animated', 'animate__fadeInDown', 'animate__slower');
    }
    if (heroHeading) {
        heroHeading.classList.remove('hide');
        heroHeading.classList.add('animate__animated', 'animate__fadeIn', 'animate__slow');
    }
    if (ctaButtonHome) {
        ctaButtonHome.classList.remove('hide');
        ctaButtonHome.classList.add('animate__animated', 'animate__fadeInLeft', 'animate__slower');
    }
};

document.addEventListener('DOMContentLoaded', function () {
    setTimeout(function () {
        const modal = document.getElementById('eventModal');
        const closeBtn = document.getElementById('closeModal');

        modal.style.display = 'block';

        closeBtn.onclick = function () {
            modal.style.display = 'none';
        };

        window.onclick = function (event) {
            if (event.target === modal) {
            modal.style.display = 'none';
            }
        };
    }, 5000); // show after 5 seconds
});