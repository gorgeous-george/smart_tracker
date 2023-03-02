$(document).ready(function(){

    // Set cache = false for all jquery ajax requests.
    $.ajaxSetup({
        cache: false,
    });

})

$(function () {

  /* Functions */

  var CreateStarterPack = function () {
    var btn = $(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      success: function () {
        window.location.reload();
      }
    });
  };

  /* Binding */

  // Create dataset
  $(".js-dataset-starter-pack").click(CreateStarterPack);

});