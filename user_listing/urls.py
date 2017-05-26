# App Imports
import views

# Django Imports
from django.conf.urls import url


urlpatterns = [
    #  App APIs #

    # User Listing
    url(r'^(?P<username>[a-z A-Z 0-9]+)/$', views.listing, name='user-listing'),
    url(r'^(?P<username>[a-z A-Z 0-9]+)/list/$', views.listing, name='user-listing'),

    # User Register
    url(r'^(?P<username>[a-z A-Z 0-9]+)/register/$', views.register, name='user-register'),

    # Add Company
    url(r'^(?P<username>[a-z A-Z 0-9]+)/add/(?P<company_domain>[a-z A-Z 0-9 \/ .]+)/$',
        views.add_company, name='user-add-company'),

    # Remove Company
    url(r'^(?P<username>[a-z A-Z 0-9]+)/remove/(?P<company_domain>[a-z A-Z 0-9 \/ .]+)/$',
        views.remove_company, name='user-remove-company'),
]
