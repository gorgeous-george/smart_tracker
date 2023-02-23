$(document).ready(function(){

    // Set cache = false for all jquery ajax requests.
    $.ajaxSetup({
        cache: false,
    });

})

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

  var reload_dataset_objects_table = function () {
    $.ajax({
      url: 'objects/reload/',
      type: 'get',
      dataType: 'json',
      success: function (data) {
        $("#dataset-object-table tbody").html(data.html_dataset_object_list);
      }
    });
  };

  var get_dataset_objects = function () {
    var btn = $(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      success: function (data) {
        $("#dataset-object-table tbody").html(data.html_dataset_object_list);
      }
    });
  };


  /* Binding */

  // Create dataset
  $(".js-create-dataset").click(loadForm);
  $("#modal-sandbox").on("submit", ".js-dataset-create-form", saveForm);

  // Update dataset and reload objects table
  $("#dataset-table").on("click", ".js-update-dataset", loadForm);
  $("#modal-sandbox").on("submit", ".js-dataset-update-form", saveForm);
  $("#modal-sandbox").on("submit", ".js-dataset-update-form", reload_dataset_objects_table);

  // Delete dataset and reload objects table
  $("#dataset-table").on("click", ".js-delete-dataset", loadForm);
  $("#modal-sandbox").on("submit", ".js-dataset-delete-form", saveForm);
  $("#modal-sandbox").on("submit", ".js-dataset-delete-form", reload_dataset_objects_table);

  // Filter objects table by selected dataset
  $(".js-show-objects").click(get_dataset_objects);

  // Clear filter, i.e. show all objects
  $(".js-show-all-objects").click(get_dataset_objects);


});