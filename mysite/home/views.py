from django.shortcuts import render,redirect
from django.views import View
from django.conf import settings
from django.contrib.auth import login, authenticate
from home.forms import registration_form
from django.contrib.auth.decorators import login_required
# Create your views here.
# This is a little complex because we need to detect when we are
# running in various configurations


class HomeView(View):
    def get(self, request):
        print(request.get_host())
        host = request.get_host()
        islocal = host.find('localhost') >= 0 or host.find('127.0.0.1') >= 0
        context = {
            'installed': settings.INSTALLED_APPS,
            'islocal': islocal
        }
        return render(request, 'home/main.html', context)

def register(response):
    if response.method == "POST":
        form = registration_form(response.POST)
        if form.is_valid():
            form.save()
            return redirect("/home")
    else:
        form = registration_form()
    return render(response,"home/signup.html",{"form":form})


    
