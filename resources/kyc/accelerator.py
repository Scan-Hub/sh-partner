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
from schemas.kyc import AcceleratorForm


class AcceleratorResource(Resource):
    @security.http(
        login_required=True,
        form_data=AcceleratorForm()
    )
    def post(self, form_data, user):
        if KYCHelper.in_preview(user_id=get(user, '_id')):
            raise BadRequest(msg="Your profile is under review. You cannot edit.")
        KYCHelper.submit(
            user_id=get(user, '_id'),
            kyc_type=KYCTypes.ACCELERATOR,
            form=form_data
        )
        return {
            'status': KYCStatus.SUBMITTED
        }
