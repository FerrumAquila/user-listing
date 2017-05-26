# App Imports
import views as app_views
import docs as app_docs

# Django Imports
from django.conf.urls import url


urlpatterns = [
    url(r'^home/$', app_views.home, name='core-home'),
    url(r'^login/$', app_views.sign_in, name='core-sign-in'),
    url(r'^logout/$', app_views.sign_out, name='core-sign-out'),
    url(r'^$', app_views.home, name='core-home'),
] + app_docs.urlpatterns
