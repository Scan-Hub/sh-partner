# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from flask_restful import Resource
from pydash import get

from connect import security
from enums.kyc import KYCTypes, KYCStatus
from helper.kyc import KYCHelper
from lib import BadRequest
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


class RootKYCResource(Resource):

    @security.http(
        login_required=True,
        response=KYCResponse()
    )
    def get(self, user):
        _kyc = KYCHelper.form_of(user_id=get(user, '_id'))
        _kyc_type = get(_kyc, 'type')
        _schema = get(_kyc_schemas, _kyc_type)
        if not _schema:
            return {
                'status': KYCStatus.NOT_START
            }
        _form = get(_kyc, 'form')
        _kyc['form'] = _schema.load(_form)
        return _kyc
