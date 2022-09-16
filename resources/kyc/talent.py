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
from enums.kyc import KYCTypes, KYCStatus, DeveloperTypes
from helper.kyc import KYCHelper
from lib import BadRequest
from schemas.kyc import DevelopForm


class TalentResource(Resource):
    @security.http(
        login_required=True,
        form_data=DevelopForm()
    )
    def post(self, form_data, user):
        if KYCHelper.in_preview(user_id=get(user, '_id')):
            raise BadRequest(msg="Your profile is under review. You cannot edit.")
        # _type = get(form_data, 'type')
        # _data = request.json
        # _form_schema = None
        #
        # if _type == DeveloperTypes.INDIVIDUAL:
        #     _form_schema = DeveloperForm()
        #
        # if _type == DeveloperTypes.TEAM:
        #     _form_schema = DeveloperAgencyForm()
        #
        # _validate = _form_schema.validate(_data)
        #
        # if _validate:
        #     _errors = _validate if isinstance(_validate, list) else [_validate]
        #     raise BadRequest(msg="Invalid data", errors=_errors)
        #
        # _form = _form_schema.dump(_data)
        #
        # _form['type'] = _type

        KYCHelper.submit(
            user_id=get(user, '_id'),
            kyc_type=KYCTypes.DEVELOPER,
            form=form_data
        )
        return {
            'status': KYCStatus.SUBMITTED
        }
