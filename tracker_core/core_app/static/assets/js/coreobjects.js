$(function () {

  /* Functions */

  var loadForm = function () {
    var btn = $(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $("#modal-coreobject .modal-content").html("");
        $("#modal-coreobject").modal("show");
      },
      success: function (data) {
        $("#modal-coreobject .modal-content").html(data.html_form);
      }
    });
  };

  var saveForm = function () {
    var form = $(this);
    $.ajax({
      url: form.attr("action"),
      data: form.serialize(),
      type: form.attr("method"),
      dataType: 'json',
      success: function (data) {
        if (data.form_is_valid) {
          $("#coreobject-table tbody").html(data.html_coreobject_list);
          $("#modal-coreobject").modal("hide");
        }
        else {
          $("#modal-coreobject .modal-content").html(data.html_form);
        }
      }
    });
    return false;
  };


  /* Binding */

  // Create coreobject
  $(".js-create-coreobject").click(loadForm);
  $("#modal-coreobject").on("submit", ".js-coreobject-create-form", saveForm);

  // Update coreobject
  $("#coreobject-table").on("click", ".js-update-coreobject", loadForm);
  $("#modal-coreobject").on("submit", ".js-coreobject-update-form", saveForm);

  // Delete coreobject
  $("#coreobject-table").on("click", ".js-delete-coreobject", loadForm);
  $("#modal-coreobject").on("submit", ".js-coreobject-delete-form", saveForm);

});