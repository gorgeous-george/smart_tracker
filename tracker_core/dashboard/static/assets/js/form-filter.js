$(document).ready(function(){

    // Set cache = false for all jquery ajax requests.
    $.ajaxSetup({
        cache: false,
    });

})

$(function () {

  /* Functions */

    var FilterObjects = function () {
    var form = $(this);
    $.ajax({
      url: form.attr("action"),
      data: form.serialize(),
      type: form.attr("method"),
      dataType: 'json',
      success: function (data) {
        if (data.form_is_valid) {
          $("#coreobject-table tbody").html(data.html_coreobject_list);
        }
      }
    });
    return false;
  };

  /* Binding */

  // Filter-form
  $("#form-filter").on("submit", ".js-filter-form-submit", FilterObjects);

});