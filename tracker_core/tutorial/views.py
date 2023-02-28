from django.shortcuts import render

# todo: add a Class with @login_required and @permission_required decorators for all view functions in this module


def tutorial(request):
    return render(request, 'tutorial.html')
