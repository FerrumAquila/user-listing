# App Imports
import models
from models import CompanyJSON
from company_listing.aetos.responses import success_response

# Django Imports
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def search_company(request, company_domain):
    company = models.CompanyCoordinator.get_from_domain(company_domain)
    json_company = CompanyJSON(company).required_json
    return success_response('Success', json_company)

