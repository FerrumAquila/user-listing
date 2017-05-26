# Packaged Imports
import json
import clearbit
from aetos_serialiser.serialisers import Serializer
from aetos_serialiser.helpers import instance_reducer

# Django Imports
from django.db import models

attrs = {
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
attrs.update({'__module__': 'company.models'})

Company = type("Company", (models.Model,), attrs.copy())


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
    def get_from_domain(cls, domain):
        companies = Company.objects.filter(domain=domain)
        if companies:
            company = companies.latest('id')
        else:
            company = cls.save_from_api(domain)
        return company

    @classmethod
    def update(cls, company):
        return cls.save_from_api(company.domain, force=True)

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


class CompanyJSON(Serializer):
    BODY_MAP = {
        'category': ('category', json.loads),
        'crunchbase': ('crunchbase', json.loads),
        'description': ('description', lambda x: x),
        'domain': ('domain', lambda x: x),
        'domainAliases': ('domainAliases', lambda x: x),
        'similarDomains': ('similarDomains', lambda x: x),
        'emailProvider': ('emailProvider', bool),
        'facebook': ('facebook', json.loads),
        'foundedYear': ('foundedYear', int),
        'geo': ('geo', json.loads),
        'api_id': ('id', lambda x: x),
        'indexedAt': ('indexedAt', lambda x: x),
        'legalName': ('legalName', lambda x: x),
        'linkedin': ('linkedin', json.loads),
        'location': ('location', lambda x: x),
        'logo': ('logo', lambda x: x),
        'metrics': ('metrics', json.loads),
        'name': ('name', lambda x: x),
        'phone': ('phone', json.loads),
        'site': ('site', json.loads),
        'tags': ('tags', lambda x: x),
        'tech': ('tech', lambda x: x),
        'ticker': ('ticker', json.loads),
        'timeZone': ('timeZone', lambda x: x),
        'twitter': ('twitter', json.loads),
        'type': ('type', lambda x: x),
        'utcOffset': ('utcOffset', int),
    }
    REDUCER = instance_reducer

