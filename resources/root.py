# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from flask import request
from flask_restful import Resource
from pydash import get

from connect import security
from helper.partner import PartnerHelper
from schemas.partner import QueryPartner, ResponsePartners


class RootResource(Resource):

    @security.http(
        login_required=False,
        params=QueryPartner(),
        response=ResponsePartners()
    )
    def get(self, params):
        _result = PartnerHelper.get_partners(partner_type=get(params, 'type'),
                                          page_size=get(params, 'page_size'),
                                          page=get(params, 'page'), params=request.args.to_dict())
        return _result