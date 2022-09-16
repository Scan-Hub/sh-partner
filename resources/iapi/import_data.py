# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from bson import ObjectId
from flask import request
from flask_restful import Resource
from pydash import get

from connect import security
from enums.kyc import KYCTypes
from helper.partner import PartnerHelper
from lib import BadRequest
from models import PartnerModel
from schemas.kyc import KYCResponse, LaunchpadForm, CompanyForm, DevelopForm, MarketingAgencyForm, AcceleratorForm, \
    IncubatorForm, VCForm

_kyc_schemas = {
    KYCTypes.LAUNCHPAD: LaunchpadForm(),
    KYCTypes.COMPANY: CompanyForm(),
    KYCTypes.DEVELOPER: DevelopForm(),
    KYCTypes.MARKETING: MarketingAgencyForm(),
    KYCTypes.ACCELERATOR: AcceleratorForm(),
    KYCTypes.INCUBATOR: IncubatorForm(),
    KYCTypes.CAPITAL: VCForm()
}


class ImportResource(Resource):

    @security.http(
        login_required=False
    )
    def post(self):
        _data = request.json
        _schema = get(_kyc_schemas, get(_data, 'type'))
        _v = _schema.validate(get(_data, 'form'))
        if _v:
            raise BadRequest(errors=[_v])
        _form = _schema.load(get(_data, 'form'))

        PartnerModel.insert_one({
            'user_id': ObjectId(),
            'detail': _form,
            'type': get(_data, 'type'),
            'created_by': 'fake_data'
        })
        return {
            'status': 'done'
        }
