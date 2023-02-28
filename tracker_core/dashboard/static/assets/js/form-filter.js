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
          url: 'filtered/',
          data: form.serialize(),
          type: form.attr("method"),
          dataType: 'json',
          success: function (data) {
            if (data.form_is_valid) {
              $("#coreobject-table tbody").html(data.html_coreobject_list);

              var chart_data = google.visualization.arrayToDataTable(data.html_chart_data);
              var options = {
                title: '',
                is3D: false,
                pieHole: 0.5,
                chartArea:{left:20,top:20,width:'100%',height:'100%'},
                colors:['#dc4c64','#e4a11b','#14a44d']
              };
              var chart = new google.visualization.PieChart(document.getElementById('piechart_3d'));
              chart.draw(chart_data, options);

            }
          }
        });
        return false;
  };



  /* Binding */

  // Filter-form
  $("form#form-filter").submit(FilterObjects);

});