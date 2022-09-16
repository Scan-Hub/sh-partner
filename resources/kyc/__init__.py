# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from .company import CompanyResource
from .root import RootKYCResource
from .capital import CapitalResource
from .accelerator import AcceleratorResource
from .talent import TalentResource
from .incubator import IncubatorResource
from .launchpad import LaunchpadResource
from .marketing import MarketingResource

kyc_resources = {
    '/capital': CapitalResource,
    '/company': CompanyResource,
    '/accelerator': AcceleratorResource,
    '/talent': TalentResource,
    '/incubator': IncubatorResource,
    '/marketing': MarketingResource,
    '/launchpad': LaunchpadResource,
    # '/': RootKYCResource,
    '': RootKYCResource
}
