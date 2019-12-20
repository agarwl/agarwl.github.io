function checkmenu() {
  if (window.innerWidth < 550) {
    var slideout = new Slideout({
      'panel': document.getElementById('panel'),
      'menu': document.getElementById('menu'),
      'padding': 150,
      'tolerance': 70,
    });

    // Toggle button
    document.querySelector('.toggle-button').addEventListener('click', function() {
      slideout.toggle();
    });
  } else {
    if (typeof slideout !== 'undefined') {
      slideout.destroy();
    }
  }
}

$(document).ready(function(){
checkmenu();
window.onresize = checkmenu;
});

