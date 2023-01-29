***
### 1. bug-0001 Feather icon is missed after ajax GET request

- http://127.0.0.1:8000/app/objects/
- coreobjects.js
```
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
  
  
$("#modal-coreobject").on("submit", ".js-coreobject-update-form", saveForm);
```
- html template
```
<button type="button"
    class="btn btn-warning btn-sm js-update-coreobject"
    data-url="{% url 'coreobject-update' coreobject.id %}">
    <span data-feather="edit" class="align-text-bottom"></span>
    Edit
</button>
```
- view
```
def save_coreobject_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            page_obj = coreobject_paginator(request)
            data['html_coreobject_list'] = render_to_string('includes/partial_coreobject_list.html', {
                'page_obj': page_obj,
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)
```
### after submitting the modal form, the icons <span data-feather="edit" and "delete" are not rendered, and consequently are not shown on the website. 
- This bug affects the 'Delete' button as well.
- <img src="bug_0001_3_icon_is_not_rendered.png">
- <img src="bug_0001_2_form_is_submitted.png">
- <img src="bug_0001_1_icon_is_rendered.png">
***
### 2. bug-0002
- tbd
