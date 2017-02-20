$(document).ready(function(){
  $.getJSON( "./package.json", function( data ) {
    $("#version").text(data.version);
  });
});
