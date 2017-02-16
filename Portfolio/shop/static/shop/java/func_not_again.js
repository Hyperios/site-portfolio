$(document).ready(function() {
  $('.pag_click > a').on('click', function(event) {
    event.stopPropagation();
    event.preventDefault();
  });
});