// JavaScript functionality for your Django project

// DOM Ready
document.addEventListener("DOMContentLoaded", function () {
    console.log("JavaScript is loaded and ready!");

    // Example: Navigation active link highlighting
    const navLinks = document.querySelectorAll("header nav ul li a");
    navLinks.forEach(link => {
        if (link.href === window.location.href) {
            link.style.fontWeight = "bold";
            link.style.textDecoration = "underline";
        }
    });
});
