# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from flask_restful import Resource
from pydash import get

from connect import security
from enums.kyc import KYCStatus, KYCTypes
from helper.kyc import KYCHelper
from lib import BadRequest
from schemas.kyc import CompanyForm, MarketingAgencyForm


class MarketingResource(Resource):
    @security.http(
        login_required=True,
        form_data=MarketingAgencyForm()
    )
    def post(self, form_data, user):
        if KYCHelper.in_preview(user_id=get(user, '_id')):
            raise BadRequest(msg="Your profile is under review. You cannot edit.")
        KYCHelper.submit(
            user_id=get(user, '_id'),
            kyc_type=KYCTypes.MARKETING,
            form=form_data
        )
        return {
            'status': KYCStatus.SUBMITTED
        }
