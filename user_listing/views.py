# App Imports
import models
from models import UserListingJSON
from company.models import CompanyJSON, CompanyCoordinator
from company_listing.aetos.responses import success_response

# Django Imports
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def listing_dashboard(request, username):
    user_listing = models.UserListingCoordinator.get_listed_companies(username)
    json_user_listing = [CompanyJSON(company).required_json for company in user_listing]
    return render_to_response('user_listing/list.html', {
        'listing': json_user_listing,
        'side_list': [object],
        'username': username
    })


@csrf_exempt
def register(request, username):
    new_user_listing = models.UserListingCoordinator.register_user_listing(username)
    json_new_user_listing = UserListingJSON(new_user_listing).required_json
    return success_response('Success', json_new_user_listing)


@csrf_exempt
def listing(request, username):
    user_listing = models.UserListingCoordinator.get_listed_companies(username)
    json_user_listing = [CompanyJSON(company).required_json for company in user_listing]
    return success_response('Success', json_user_listing)


@csrf_exempt
def add_company(request, username, company_domain):
    models.UserListingCoordinator.add_companies(username, company_domain)
    company = CompanyCoordinator.get_from_domain(company_domain)
    json_company = CompanyJSON(company).required_json
    return success_response('Success', json_company)


@csrf_exempt
def remove_company(request, username, company_domain):
    models.UserListingCoordinator.remove_companies(username, company_domain)
    company = CompanyCoordinator.get_from_domain(company_domain)
    json_company = CompanyJSON(company).required_json
    return success_response('Success', json_company)
