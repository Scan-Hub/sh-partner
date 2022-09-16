# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
import traceback
from datetime import datetime

from marshmallow import Schema, EXCLUDE, fields, validate, RAISE, validates_schema, ValidationError
from pydash import get

from enums.status import OperatingStatus, ProjectStatus
from lib import NotBlank, DatetimeField
from schemas.utils import Phone
from static import countries


class StrToDatetimeField(fields.Field):

    def __init__(self, format, *args, **kwargs):
        self.format = format

        super(StrToDatetimeField, self).__init__(*args, **kwargs)

    default_error_messages = {
        "invalid": "Invalid data format DD/MM/YYYY.",
        "invalid_utf8": "Not a valid utf-8 string.",
        'year': "Invalid year."
    }

    def _serialize(self, value, attr, obj, **kwargs):
        return value

    def _deserialize(
            self,
            value,
            *args,
            **kwargs
    ):
        try:
            _date = datetime.strptime(value, self.format)
            if _date.year > datetime.now().year:
                raise self.make_error('year')
            return value
        except:
            raise self.make_error('invalid')


class CommunitySchema(Schema):
    class Meta:
        unknown = EXCLUDE

    code = fields.Str(required=True, validate=validate.OneOf([
        'medium',
        'twitter',
        'linkedin',
        'telegram',
        'instagram',
        'facebook',
        'discord',
        'youtube'
    ]))
    link = fields.URL(required=True)

    # medium = fields.URL(default='')
    # twitter = fields.URL(default='')
    # linkedin = fields.URL(default='')
    # telegram = fields.URL(default='')


class Member(Schema):
    class Meta:
        unknown = EXCLUDE

    name = fields.Str(required=True, validate=NotBlank())
    title = fields.Str(required=True, validate=NotBlank())
    email = fields.Email(required=True)
    image = fields.URL(required=True)
    # Optional
    phone = fields.Nested(Phone)
    linkedin = fields.URL(allow_none=True)
    hidden_fields = fields.List(fields.Str(), default=[])


class Partner(Schema):
    class Meta:
        unknown = EXCLUDE

    name = fields.Str(required=True, validate=NotBlank())
    logo = fields.URL(required=True)
    website = fields.URL(required=True)


class Portfolio(Schema):
    class Meta:
        unknown = EXCLUDE

    logo = fields.URL(required=True)
    name = fields.Str(required=True, validate=NotBlank())
    website = fields.URL(required=True)
    social_media = fields.List(fields.Nested(CommunitySchema), required=True, validate=validate.Length(min=1))
    # operating_status = fields.Str(required=True,
    #                               validate=validate.OneOf([OperatingStatus.ACTIVE, OperatingStatus.CLOSE]))


class BaseInfo(Schema):
    class Meta:
        unknown = EXCLUDE

    logo = fields.URL(required=True)
    name = fields.Str(required=True, validate=NotBlank())
    website = fields.URL(required=True)
    country = fields.Str(required=True, validate=validate.OneOf(
        [get(x, 'code') for x in countries]))  # https://gist.github.com/keeguon/2310008
    location = fields.Str(required=True, validate=NotBlank())
    email = fields.Email(required=True)

    founded_date = DatetimeField(required=True)

    number_of_employees = fields.Int(required=True, validate=validate.Range(min=1))

    business_registration_certificate = fields.URL(required=True)
    team_members = fields.List(fields.Nested(Member), required=True, validate=validate.Length(min=1))
    operating_status = fields.Str(required=True,
                                  validate=validate.OneOf([OperatingStatus.ACTIVE, OperatingStatus.CLOSE]))
    about_company = fields.Str(required=True, validate=[NotBlank(), validate.Length(max=20000)])
    # Optional
    founder_ids = fields.List(fields.URL(), default=[])
    phone = fields.Nested(Phone)
    community = fields.List(fields.Nested(CommunitySchema), default=[], missing=[])
    portfolios = fields.List(fields.Nested(Portfolio), default=[], missing=[])
    hidden_fields = fields.List(fields.Str(), default=[])
    partners = fields.List(fields.Nested(Partner), default=[], missing=[])


class PortfolioStatus(Portfolio):
    status = fields.Str(required=True,
                        validate=validate.OneOf([OperatingStatus.ACTIVE, OperatingStatus.CLOSE]))


class PortfolioCompanyStatus(Portfolio):
    status = fields.Str(required=True,
                        validate=validate.OneOf([ProjectStatus.IN_PROGRESS,
                                                 ProjectStatus.COMPLETED]))


class CompanyForm(BaseInfo):
    class Meta:
        unknown = RAISE

    number_of_investment_received = fields.Float(required=True, validate=validate.Range(min=0))
    total_fund_received = fields.Float(required=True, validate=validate.Range(min=0))

    industries = fields.List(fields.Str(validate=NotBlank()), required=True, validate=validate.Length(min=1))
    portfolios = fields.List(fields.Nested(PortfolioCompanyStatus), default=[], missing=[])


class PortfolioDev(Schema):
    class Meta:
        unknown = EXCLUDE

    logo = fields.URL(required=True)
    name = fields.Str(required=True, validate=NotBlank())
    link = fields.URL(required=True)
    title = fields.Str(required=True, validate=NotBlank())
    community = fields.List(fields.Nested(CommunitySchema), required=True, validate=validate.Length(min=1))


class Experience(Schema):
    class Meta:
        unknown = EXCLUDE

    start_date = DatetimeField(required=True)
    end_date = DatetimeField(required=True)
    company_name = fields.Str(required=True, validate=NotBlank())
    title = fields.Str(required=True, validate=NotBlank())
    employment_type = fields.Str(required=True, validate=validate.OneOf([
        'full_time',
        'part_time',
        'self_employed',
        'seasonal',
        'internship_part_time'
    ]))
    industry = fields.Str(required=True, validate=NotBlank())
    location = fields.Str(required=True, validate=NotBlank())
    portfolio = fields.List(fields.Nested(PortfolioDev), missing=[])


class Education(Schema):
    class Meta:
        unknown = EXCLUDE

    school = fields.Str(required=True, validate=validate.OneOf([
        'native_fluent',
        'advanced',
        'intermediate',
        'basic'
    ]))
    degree = fields.Str(required=True, validate=validate.OneOf([
        'transfer',
        'associate',
        'bachelor',
        'graduate',
        'master',
        'doctoral',
        'professional',
        'specialist'
    ]))
    field_of_study = fields.Str(required=True, validate=NotBlank())
    start_date = DatetimeField(required=True)
    end_date = DatetimeField(default=None, allow_none=True)
    grade = fields.Str(required=True, validate=validate.OneOf([
        'excellent',
        'very_good',
        'good',
        'satisfactory',
        'pass',
        'conditional',
        'fail',
        'incomplete'
    ]))
    certificate = fields.URL(default=None, allow_none=True)


class DevelopForm(Schema):
    class Meta:
        unknown = RAISE

    first_name = fields.Str(required=True, validate=NotBlank())
    last_name = fields.Str(required=True, validate=NotBlank())
    avatar = fields.URL(required=True)
    location = fields.Str(required=True, validate=NotBlank())

    email = fields.Email(required=True)
    phone = fields.Nested(Phone)
    primary_job_titles = fields.List(fields.Str(), required=True, validate=validate.Length(min=1))
    community = fields.List(fields.Nested(CommunitySchema), required=True, validate=validate.Length(min=1))
    description = fields.Str(required=True, validate=[NotBlank(), validate.Length(max=20000)])
    experiences = fields.List(fields.Nested(Experience), required=True)
    english_proficiency = fields.Str(required=True, validate=validate.OneOf([
        'native_fluent',
        'advanced',
        'intermediate',
        'basic'
    ]))
    skills = fields.List(fields.Str(), required=True)
    other_languages = fields.List(fields.Str(), required=True)

    educations = fields.List(fields.Nested(Education), required=True)
    hidden_fields = fields.List(fields.Str(), default=[], missing=[])


class VCForm(BaseInfo):
    class Meta:
        unknown = EXCLUDE

    sectors_of_investment = fields.List(fields.Str(), required=True, validate=validate.Length(min=1))
    stage_of_investment = fields.List(fields.Str(), required=True, validate=validate.Length(min=1))
    total_number_of_investment = fields.Int(required=True, validate=validate.Range(min=0))
    total_funding_amount = fields.Float(required=True, validate=validate.Range(min=0))
    other_categories = fields.List(fields.Str(), default=[], missing=[])


class MarketingAgencyForm(BaseInfo):
    class Meta:
        unknown = RAISE

    marketing_sectors = fields.List(fields.Str(), required=True, validate=validate.Length(min=1))


class LaunchpadForm(BaseInfo):
    class Meta:
        unknown = RAISE

    category = fields.Str(required=True, validate=NotBlank())
    platforms = fields.List(fields.Str(), required=True)
    launching_sectors = fields.List(fields.Str(), required=True)
    number_of_tge = fields.Int(default=0)
    total_fund_raise = fields.Float(default=0, validate=validate.Range(min=0))


class IncubatorForm(BaseInfo):
    class Meta:
        unknown = RAISE

    sectors_of_incubator = fields.List(fields.Str(), required=True)
    stage_of_incubator = fields.Str(required=True, validate=NotBlank())

    number_of_project_incubated = fields.Int(required=True, validate=validate.Range(min=0))
    total_fund_raise = fields.Float(required=True, validate=validate.Range(min=0))
    portfolios = fields.List(fields.Nested(PortfolioStatus), default=[], missing=[])


class AcceleratorForm(BaseInfo):
    class Meta:
        unknown = RAISE

    sectors_of_accelerator = fields.List(fields.Str(), required=True)
    stage_of_accelerator = fields.Str(required=True, validate=NotBlank())
    number_of_investment_received = fields.Int(required=True, validate=validate.Range(min=0))
    total_fund_received = fields.Float(required=True, validate=validate.Range(min=0))
    portfolios = fields.List(fields.Nested(PortfolioStatus), default=[], missing=[])


class KYCResponse(Schema):
    class Meta:
        unknown = EXCLUDE

    status = fields.Str()
    form = fields.Dict()
    type = fields.Str()
