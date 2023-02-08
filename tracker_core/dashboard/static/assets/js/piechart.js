$(function () {

  /* Functions */




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