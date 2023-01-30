from auth_core.forms import RegisterForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import DetailView, FormView, UpdateView


class RegisterFormView(SuccessMessageMixin, FormView):
    """
    Class-based view representing Register form for a new user
    """
    template_name = 'registration/register.html'
    form_class = RegisterForm
    success_message = "Profile has been registered"
    success_url = reverse_lazy("index")

    def form_valid(self, form):
        """
        Form validation, and manual adding a new User to the database,
        and further authentication and authorization of the User
        """
        user = form.save()
        password = form.cleaned_data.get("password1")
        user = authenticate(username=user.username, password=password)
        login(self.request, user)
        return super(RegisterFormView, self).form_valid(form)


class UpdateProfile(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """
    Class-based view representing Profile Update feature
    """
    model = User
    fields = ["username", "email"]
    template_name = 'registration/update_profile.html'
    success_url = reverse_lazy("index")
    success_message = "Profile updated"

    def get_object(self, queryset=None):
        """
        Returning User object
        """
        user = self.request.user
        return user


class UserProfile(LoginRequiredMixin, DetailView):
    """
    Class-based view representing User Profile feature
    """
    model = User
    template_name = "registration/profile.html"

    def get_object(self, queryset=None):
        """
        Returning User object
        """
        user = self.request.user
        return user

    def get_context_data(self, **kwargs):
        """
        Returning User object's context data
        """
        context = super(UserProfile, self).get_context_data(**kwargs)
        return context
