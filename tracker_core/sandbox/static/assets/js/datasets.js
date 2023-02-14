$(function () {

  /* Functions */

  var loadForm = function () {
    var btn = $(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $("#modal-sandbox .modal-content").html("");
        $("#modal-sandbox").modal("show");
      },
      success: function (data) {
        $("#modal-sandbox .modal-content").html(data.html_form);
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
          $("#dataset-table tbody").html(data.html_dataset_list);
          $("#modal-sandbox").modal("hide");
        }
        else {
          $("#modal-sandbox.modal-content").html(data.html_form);
        }
      }
    });
    return false;
  };


  /* Binding */

  // Create coreobject
  $(".js-create-dataset").click(loadForm);
  $("#modal-sandbox").on("submit", ".js-dataset-create-form", saveForm);

  // Update coreobject
  $("#dataset-table").on("click", ".js-update-dataset", loadForm);
  $("#modal-sandbox").on("submit", ".js-dataset-update-form", saveForm);

  // Delete coreobject
  $("#dataset-table").on("click", ".js-delete-dataset", loadForm);
  $("#modal-sandbox").on("submit", ".js-dataset-delete-form", saveForm);

});