# Django Imports
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt



@csrf_exempt
def user_list(request, username):
    print 'get listing of "%s"' % username
    return render_to_response("user_listing/list.html", {})


