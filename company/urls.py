# App Imports
import views

# Django Imports
from django.conf.urls import url


urlpatterns = [
    # App APIs #

    # Search Company
    url(r'^search/(?P<company_domain>[a-z A-Z 0-9 \/ .]+)/$', views.search_company, name='company-search'),
]
