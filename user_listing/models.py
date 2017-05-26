from __future__ import unicode_literals
# App Imports
from company.models import Company
from company_listing.aetos.models import CustomModel
from company.models import CompanyCoordinator as CompCoor

# Django Imports
from django.db import models


class UserListing(CustomModel):
    companies = models.ManyToManyField(Company, related_name='tagged_by')
    username = models.CharField(max_length=63, unique=True)


class UserListingCoordinator(object):
    @classmethod
    def get_listing(cls, username):
        return UserListing.objects.get(username=username)

    @classmethod
    def register_user_listing(cls, username):
        user_listing = UserListing(username=username, is_active=True)
        user_listing.save()
        return user_listing

    @classmethod
    def get_listed_companies(cls, username, update=False):
        listing = cls.get_listing(username)
        listed_companies = listing.companies.all()
        if not update:
            return list(listed_companies)
        else:
            return [CompCoor.update(company) for company in listed_companies]

    @classmethod
    def add_companies(cls, username, companies):
        listing = cls.get_listing(username)
        if not isinstance(companies, list):
            companies = [companies]
        for company in companies:
            listing.companies.add(CompCoor.get_from_domain(company))

    @classmethod
    def remove_companies(cls, username, companies):
        listing = cls.get_listing(username)
        if not isinstance(companies, list):
            companies = [companies]
        for company in companies:
            listing.companies.remove(CompCoor.get_from_domain(company))
