# App Imports
import models
from company_listing.aetos.responses import success_response
from company.models import CompanyJSON

# Django Imports
import json
import jsonpickle
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def register(request, username):
    new_user_listing = models.UserListingCoordinator.register_user_listing(username)
    return success_response('Success', new_user_listing)


@csrf_exempt
def listing(request, username):
    user_listing = models.UserListingCoordinator.get_listed_companies(username)
    json_user_listing = [CompanyJSON(company).required_json for company in user_listing]
    return success_response('Success', json_user_listing)


@csrf_exempt
def add_company(request, username, company_domain):
    models.UserListingCoordinator.add_companies(username, company_domain)
    return success_response('Success', dict())


@csrf_exempt
def remove_company(request, username, company_domain):
    models.UserListingCoordinator.remove_companies(username, company_domain)
    return success_response('Success', dict())
