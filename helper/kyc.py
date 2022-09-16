# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from pydash import get

from enums.kyc import KYCStatus
from models import KYCModel


class KYCHelper:

    @staticmethod
    def submitted(user_id):
        if KYCModel.find_one({
            'user_id': user_id
        }):
            return True
        return False

    @staticmethod
    def form_of(user_id):
        return KYCModel.find_one({
            'user_id': user_id
        })

    @staticmethod
    def in_preview(user_id):
        _kyc = KYCModel.find_one({
            'user_id': user_id
        })
        if get(_kyc, 'status') == KYCStatus.IN_REVIEW:
            return True
        return False

    @staticmethod
    def submit(user_id, kyc_type, form):
        KYCModel.update_one({
            'user_id': user_id
        }, obj={
            'updated_by': str(user_id),
            'type': kyc_type,
            'form': form,
            'status': KYCStatus.SUBMITTED
        }, upsert=True, worker=True)
