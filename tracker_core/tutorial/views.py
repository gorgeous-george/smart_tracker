from django.shortcuts import render
from django.views.decorators.cache import cache_page


# todo: add a Class with @login_required and @permission_required decorators for all view functions in this module

@cache_page(60 * 60)
def tutorial(request):
    return render(request, 'tutorial.html')
