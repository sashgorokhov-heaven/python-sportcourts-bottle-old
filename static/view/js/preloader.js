// makes sure the whole site is loaded
jQuery(window).ready(function() {
	// will first fade out the loading animation
	jQuery("#status").fadeOut();
	// will fade out the whole DIV that covers the website.
	jQuery("#preloader").delay(200).fadeOut("fast");
}) 