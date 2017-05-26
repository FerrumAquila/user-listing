# Packaged Imports
import json
import clearbit

# Django Imports
from django.db import models

sample_attrs = {
    '__module__': 'company.models',
    'category': models.TextField(default='{}'),
    'crunchbase': models.TextField(default='{}'),
    'description': models.CharField(max_length=1024, null=True),
    'domain': models.CharField(max_length=1024, null=True),
    'domainAliases': models.CharField(max_length=1024, null=True),
    'similarDomains': models.CharField(max_length=1024, null=True),
    'emailProvider': models.NullBooleanField(),
    'facebook': models.TextField(default='{}'),
    'foundedYear': models.IntegerField(null=True),
    'geo': models.TextField(default='{}'),
    'api_id': models.CharField(max_length=1024, null=True),
    'indexedAt': models.CharField(max_length=1024, null=True),
    'legalName': models.CharField(max_length=1024, null=True),
    'linkedin': models.TextField(default='{}'),
    'location': models.CharField(max_length=1024, null=True),
    'logo': models.CharField(max_length=1024, null=True),
    'metrics': models.TextField(default='{}'),
    'name': models.CharField(max_length=1024, null=True),
    'phone': models.TextField(default='{}'),
    'site': models.TextField(default='{}'),
    'tags': models.CharField(max_length=1024, null=True),
    'tech': models.CharField(max_length=1024, null=True),
    'ticker': models.TextField(default='{}'),
    'timeZone': models.CharField(max_length=1024, null=True),
    'twitter': models.TextField(default='{}'),
    'type': models.CharField(max_length=1024, null=True),
    'utcOffset': models.IntegerField(null=True)
}

Company = type("Company", (models.Model,), sample_attrs.copy())


class CompanyCoordinator(object):
    TYPE_MAP = {
        dict: json.dumps,
        list: lambda x: ",".join(x),
        type(None): lambda x: json.dumps('{}'),
    }

    @classmethod
    def save_in_db(cls, data_json, force=False):
        db_attrs = cls._get_db_attrs(data_json)
        company = Company(**db_attrs)
        company_exists = cls._company_exists(company)
        if company_exists:
            if force:
                company_exists.delete()
            else:
                raise Exception('Company "%s" Already Exists. Pass force=True to force update' % data_json['domain'])
        company.save()
        return company

    @classmethod
    def save_from_api(cls, domain, force=False):
        data_json = cls._get_data_json(domain)
        data_json['api_id'] = data_json['id']
        data_json.pop('id')
        return cls.save_in_db(data_json, force)

    @classmethod
    def get_company(cls, domain):
        companies = Company.objects.filter(domain=domain)
        if companies:
            company = companies.latest('id')
        else:
            company = cls.save_from_api(domain)
        return company

    @classmethod
    def _get_v(cls, v):
        return cls.TYPE_MAP[type(v)](v) if type(v) in cls.TYPE_MAP else v

    @classmethod
    def _company_exists(cls, company):
        return Company.objects.filter(domain=company.domain)

    @classmethod
    def _get_db_attrs(cls, data_json):
        return {k: cls._get_v(v) for k, v in data_json.items()}

    @classmethod
    def _get_data_json(cls, domain):
        company = clearbit.Company.find(domain=domain)
        if company is not None and 'pending' not in company:
            return company
        else:
            return dict()
