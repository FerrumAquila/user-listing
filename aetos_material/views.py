# Django Imports
from django.contrib import auth
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.core.urlresolvers import reverse


def home(request):
    return render_to_response("home.html", {})


def sign_in(request):
    if request.method == "POST" and request.user.id is None:
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse(data={"success": True})
        else:
            return JsonResponse(data={"error": "wrong username and password"})
    else:
        return render(request, "core/sign-in.html")


# For Logout, Just LogOut User
def sign_out(request):
    auth.logout(request)
    response = HttpResponseRedirect(reverse("core-sign-in"))
    response.set_cookie(key='token', value='')
    return response

