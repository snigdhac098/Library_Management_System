from django.shortcuts import render,redirect
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout,login
from django.urls import reverse_lazy
from . forms import RegistrationForm
from django.views.generic import FormView
from django.contrib import messages



# Create your views here.
class UserRegistrationForm(FormView):
    form_class = RegistrationForm
    template_name = 'form.html'
    success_url = reverse_lazy("home_page")

    def form_valid(self, form):
        user = form.save()
        login(self.request, user=user)
        messages.success(self.request, "Registration successfully completed")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["type"] = "Registration"
        return context


class userlogin(LoginView):
     template_name='login.html'
     success_url = reverse_lazy('homepage')
       
     def get_success_url(self):
          return reverse_lazy('homepage')


     def form_valid(self,form):
          return super().form_valid(form)
     def form_invalid(self,form):
          return super().form_invalid(form)
     
     def get_context_data(self, **kwargs):
          context=super().get_context_data(**kwargs)
          context['type']='Login'
          return context


def user_logout(request):
     logout(request)
     return redirect('login')
          