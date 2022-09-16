# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from marshmallow import Schema, EXCLUDE, fields, validate, INCLUDE
from pydash import get

from enums.kyc import KYCTypes
from lib import ObjectIdField


class QueryPartner(Schema):
    class Meta:
        unknown = INCLUDE

    type = fields.Str(required=True, validate=validate.OneOf([
        KYCTypes.INCUBATOR,
        KYCTypes.COMPANY,
        KYCTypes.CAPITAL,
        KYCTypes.LAUNCHPAD,
        KYCTypes.MARKETING,
        KYCTypes.DEVELOPER,
        KYCTypes.ACCELERATOR
    ]))

    page_size = fields.Int(default=20)
    page = fields.Int(default=1, validate=validate.Range(min=1))


class OverviewPartner(Schema):
    class Meta:
        unknown = EXCLUDE

    _id = ObjectIdField()
    type = fields.Str()
    detail = fields.Dict(missing={})


class ResponsePartners(Schema):
    class Meta:
        unknown = EXCLUDE

    items = fields.List(fields.Nested(OverviewPartner), missing=[])
    page = fields.Int(missing=1)
    number_of_page = fields.Int(missing=1)


class CapitalSchema(Schema):
    class Meta:
        unknown = EXCLUDE
        order = True

    name = fields.Str(missing='N/A')
    country = fields.Str(missing='N/A')
    portfolios = fields.Function(missing=0, deserialize=lambda x: len(x))
    investment = fields.Float(missing=0)
    sector = fields.Str(data_key='industry')
    rank = fields.Int(missing=0)
    logo = fields.Str(missing='')


class CompanySchema(Schema):
    class Meta:
        unknown = EXCLUDE
        order = True

    name = fields.Str(missing='N/A')
    country = fields.Str(missing='N/A')
    portfolios = fields.Function(missing=0, deserialize=lambda x: len(x))
    partners = fields.Function(missing=0, deserialize=lambda x: len(x))
    industries = fields.Function(missing='N/A', deserialize=lambda x: ', '.join(x) if isinstance(x, list) else '')
    logo = fields.Str(missing='')


class LaunchpadSchema(Schema):
    class Meta:
        unknown = EXCLUDE
        order = True

    name = fields.Str(missing='N/A')
    country = fields.Str(missing='N/A')
    portfolios = fields.Function(missing=0, deserialize=lambda x: len(x))
    category = fields.Str(missing='N/A')
    number_of_tge = fields.Int(missing=0)
    rank = fields.Int(missing=0)
    logo = fields.Str(missing='')


class IncubatorSchema(Schema):
    class Meta:
        unknown = EXCLUDE
        order = True

    name = fields.Str(missing='N/A')
    country = fields.Str(missing='N/A')
    portfolios = fields.Function(missing=0, deserialize=lambda x: len(x))
    sectors_of_incubator = fields.Function(missing='N/A',
                                           deserialize=lambda x: ', '.join(x) if isinstance(x, list) else '')
    number_of_employees = fields.Int(missing=0)
    rank = fields.Int(missing=0)
    logo = fields.Str(missing='')


class MarketingSchema(Schema):
    class Meta:
        unknown = EXCLUDE
        order = True

    name = fields.Str(missing='N/A')
    country = fields.Str(missing='N/A')
    portfolios = fields.Function(missing=0, deserialize=lambda x: len(x))
    marketing_sectors = fields.Function(missing='N/A',
                                        deserialize=lambda x: ', '.join(x) if isinstance(x, list) else '')
    rank = fields.Int(missing=0)
    logo = fields.Str(missing='')
    partners = fields.Function(missing=0, deserialize=lambda x: len(x))


class AcceleratorSchema(Schema):
    class Meta:
        unknown = EXCLUDE
        order = True

    name = fields.Str(missing='N/A')
    country = fields.Str(missing='N/A')
    portfolios = fields.Function(missing=0, deserialize=lambda x: len(x))
    sectors_of_accelerator = fields.Function(missing='N/A',
                                             deserialize=lambda x: ', '.join(x) if isinstance(x, list) else '')
    rank = fields.Int(missing=0)
    logo = fields.Str(missing='')
    partners = fields.Function(missing=0, deserialize=lambda x: len(x))


class DeveloperSchema(Schema):
    class Meta:
        unknown = EXCLUDE
        order = True

    name = fields.Str(missing='N/A')
    country = fields.Str(missing='N/A')
    portfolios = fields.Function(missing=0, deserialize=lambda x: len(x))
    degree = fields.Function(missing='N/A', data_key='educations',
                             deserialize=lambda x: ', '.join(get(x, 'degree')).capitalize() if isinstance(x,
                                                                                                          list) else '')
    rank = fields.Int(missing=0)
    logo = fields.Str(missing='')
    field_of_study = fields.Function(missing='N/A', data_key='educations',
                                     deserialize=lambda x: ', '.join(
                                         get(x, 'field_of_study')).capitalize() if isinstance(x, list) else '')
    employment_type = fields.Function(missing='N/A', data_key='experiences',
                                      deserialize=lambda x: ', '.join(get(x, 'employment_type')).replace("_",
                                                                                                         " ").capitalize() if isinstance(
                                          x, list) else '')
