'use strict';
// NOTE: HAMBURGER

const hamburger = document.querySelector('.hamburger');

hamburger.addEventListener('click', function () {
    console.log('Button clicked!');
    const bar1 = document.querySelector('.bar1');
    const bar2 = document.querySelector('.bar2');
    const bar3 = document.querySelector('.bar3');
    const nav = document.querySelector('nav');
    const menuHamburger = document.querySelector('.menu-container');

    bar1.classList.toggle('transform-bar1');
    bar2.classList.toggle('transform-bar2');
    bar3.classList.toggle('transform-bar3');
    nav.classList.toggle('nav');
    menuHamburger.classList.toggle('menu-hamburger');
});

function check_high_thresholds() {
    var elements = document.getElementsByClassName('high_threshold');
    for (var i = 0; i < elements.length; i++) {
        elements[i].style.color = "green";
        var values = elements[i].innerHTML;
        if (values >= 95) {
            elements[i].style.color = "red";
        } else if (values >= 90 && values < 95) {
            elements[i].style.color = "orange";
        }
    }
}

function check_low_thresholds() {
    var elements = document.getElementsByClassName('low_threshold');
    for (var i = 0; i < elements.length; i++) {
        elements[i].style.color = "green";
        var values = elements[i].innerHTML;
        if (values >= 15) {
            elements[i].style.color = "red";
        } else if (values >= 10 && values < 15) {
            elements[i].style.color = "orange";
        }
    }
}

function check_timestanps() {
    var elements = document.getElementsByClassName('timestamp');
    for (var i = 0; i < elements.length; i++) {
        elements[i].style.color = "green";
        var values = Date.parse(elements[i].innerHTML)
        if (Date.now() - values > 600000){
            elements[i].style.color = "red";
        } else {
            elements[i].style.color = "green";
        }
    }
}

check_low_thresholds()
check_high_thresholds()
check_timestanps()