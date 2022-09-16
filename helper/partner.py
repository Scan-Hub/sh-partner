# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
import traceback

from bson import ObjectId
from pydash import get

from enums.kyc import KYCTypes
from helper.indicator import IndicatorHelper
from lib import BadRequest
from models import PartnerModel
from schemas.partner import CapitalSchema, CompanySchema, IncubatorSchema, LaunchpadSchema, MarketingSchema, \
    AcceleratorSchema, DeveloperSchema

_detail_schemas = {
    KYCTypes.CAPITAL: CapitalSchema(),
    KYCTypes.COMPANY: CompanySchema(),
    KYCTypes.INCUBATOR: IncubatorSchema(),
    KYCTypes.LAUNCHPAD: LaunchpadSchema(),
    KYCTypes.MARKETING: MarketingSchema(),
    KYCTypes.ACCELERATOR: AcceleratorSchema(),
    KYCTypes.DEVELOPER: DeveloperSchema()
}


class Indicators:

    @classmethod
    def math(cls, query: str, value):
        try:
            if query.endswith(')'):
                _fund = query.split('(')[0]
                _indicator = getattr(IndicatorHelper, _fund)
                if _indicator:
                    return _indicator(value=value, query=query.replace(_fund, ''))
            return value == query
        except:
            traceback.print_exc()

        return True


class PartnerHelper:

    @staticmethod
    def get_partners(partner_type, page, page_size, params):
        def func_filter(item):

            if 'page' in params:
                del params['page']
            if 'page_size' in params:
                del params['page_size']
            if 'type' in params:
                del params['type']
            for key, value in params.items():
                if not Indicators.math(query=value, value=get(item, f'detail.{key}')):
                    return False

            return True

        # return {
        #     "items": [
        #         {
        #             'type': KYCTypes.CAPITAL,
        #             '_id': ObjectId(),
        #             'detail': {
        #
        #             }
        #         }
        #     ],
        #     'num_of_page': 1,
        #     'page_size': page_size,
        #     'page': page
        # }
        #
        _result = PartnerModel.page(
            filter={
                "type": partner_type
            },
            func_filter=func_filter,
            page=page,
            page_size=page_size
        )

        _schema = get(_detail_schemas, partner_type)

        def load_detail(x):
            try:
                return {
                    **x,
                    'detail': _schema.load(get(x, 'detail'))
                }
            except:
                traceback.print_exc()
                return {}
        if not get(_result, 'items'):
            _result['items'] = [{
                '_id': ObjectId(),
                'type': partner_type,
                'detail': {}
            }]
        if not _schema:
            raise BadRequest('Invalid params.', errors=[{
                'type': 'Type is not found.'
            }])
        return {
            **_result,
            'items': [x for x in [load_detail(row) for row in get(_result, 'items')] if x]
        }
