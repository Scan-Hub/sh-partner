# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from resources.health_check import HealthCheck
from resources.iapi import iapi_resources
from resources.iapi.import_data import ImportResource
from resources.kyc import kyc_resources
from resources.explore import ExploreResource

api_resources = {
    '/common/health_check': HealthCheck,
    **{f'/iapi{k}': val for k, val in iapi_resources.items()},
    **{f'/kyc{k}': val for k, val in kyc_resources.items()},
    '/explore': ExploreResource,
    '/iapi/import': ImportResource
}
