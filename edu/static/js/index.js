let body = document.body
let menuButton = document.querySelector('.menu-button');
let menu = document.querySelector('.menu');
 
menuButton.addEventListener('click', () => {
    menu.classList.toggle('display');
});
