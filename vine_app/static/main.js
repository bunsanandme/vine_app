const tabs = document.querySelectorAll('.tabs li');
const tabContentBoxes = document.querySelectorAll('#tab-content > div');

tabs.forEach((tab) => {
    tab.addEventListener('click', () => {
    tabs.forEach(item => item.classList.remove('is-active'));
    tab.classList.add('is-active');

    const target = tab.dataset.target;
    tabContentBoxes.forEach(box => {
        if (box.getAttribute('id') === target) {
        box.classList.remove('is-hidden');
        } else {
        box.classList.add('is-hidden');
        }
    })
    })
});

function closeModal($el) {
    $el.classList.remove('is-active');

}

document.addEventListener('DOMContentLoaded', () => {
    function openModal($el) {
    $el.classList.add('is-active');
    }

    function closeModal($el) {
    $el.classList.remove('is-active');
    }

    function closeAllModals() {
    (document.querySelectorAll('.modal') || []).forEach(($modal) => {
        closeModal($modal);
    });
    }

    // Add a click event on buttons to open a specific modal
    (document.querySelectorAll('.js-modal-trigger') || []).forEach(($trigger) => {
    const modal = $trigger.dataset.target;
    const $target = document.getElementById(modal);

    $trigger.addEventListener('click', () => {
        openModal($target);
    });
    });

    // Add a click event on various child elements to close the parent modal
    (document.querySelectorAll(
    '.modal-background, .modal-close, .modal-card-head .delete, .modal-card-foot .button') || []).forEach((
    $close) => {
    const $target = $close.closest('.modal');

    $close.addEventListener('click', () => {
        closeModal($target);
    });
    });

    // Add a keyboard event to close all modals
    document.addEventListener('keydown', (event) => {
    const e = event || window.event;

    if (e.keyCode === 27) { // Escape key
        closeAllModals();
    }
    });
});

let deleteMessage = function (event) {
    $('article').remove();
}

let closeWindow = function ($el) {
    $el.removeClass('is-active');
}

let hideNavbar = function (event) {
    $("#main_navbar").addClass("is-hidden")
    $("#navbar_button").removeClass("is-hidden")
}

let showNavbar = function (event) {
    $("#main_navbar").removeClass("is-hidden")
    $("#navbar_button").addClass("is-hidden")
}

var dropdown = document.querySelector('.dropdown');
dropdown.addEventListener('click', function (event) {
    event.stopPropagation();
    dropdown.classList.toggle('is-active');
})

function goBack() {
    window.history.back()
}

let loadFile = function (event) {
    let image = document.getElementById('output');
    image.src = URL.createObjectURL(event.target.files[0]);
};