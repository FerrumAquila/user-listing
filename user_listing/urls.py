# App Imports
import views

# Django Imports
from django.conf.urls import url


urlpatterns = [
    # App APIs
    url(r'^(?P<username>[a-z A-Z 0-9]+)/$', views.user_list, name='user-listing'),
]
